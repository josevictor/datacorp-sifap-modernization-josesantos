package com.datacorp.sifap.migration;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.EOFException;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.util.List;
import org.junit.jupiter.api.Test;

class LegacyBeneficiaryReaderTest {

    private static final String LAYOUT = """
        # LEVEL CODE NAME FORMAT LENGTH OCCURS OPTIONS BYTE-WIDTH
        01 AA NUM-REGISTRATION  N 11   1 DE,UQ 11
        01 AB NUM-CPF           A 11   1 DE    11
        01 AC FULL-NAME         A 20   1 -     20
        01 AF DT-BIRTH          N 8    1 DE    8
        01 AM NUM-NIS           N 11   1 DE,UQ 11
        02 BJ COD-REGION        A 2    1 DE    2
        01 CA COD-PROGRAM       A 4    1 DE    4
        01 CE STAT-BENEFICIARY  A 1    1 DE    1
        01 CH AMT-FAMILY-INCOME P 9,2  1 -     5
        01 CK QTY-DEPEND        N 2    1 -     2
        01 CL IND-DOCS-OK       A 1    1 FI    1
        # RECORD-BYTES 76
        """;

    @Test
    void should_read_every_migrated_field_at_its_declared_position() throws IOException {
        byte[] record = record(
            "10000000114",
            "78933359478",
            "MARIA MARTINS",
            "19460612",
            "28566181479",
            "02",
            "PBF1",
            "A",
            new byte[] {0x00, 0x01, 0x00, 0x00, 0x0C},
            "00",
            "S");

        List<LegacyBeneficiaryRecord> records = read(concat(record, separator()));

        assertEquals(1, records.size());
        LegacyBeneficiaryRecord first = records.get(0);
        assertAll(
            () -> assertEquals(1L, first.lineNumber()),
            () -> assertEquals("10000000114", first.registration()),
            () -> assertEquals("78933359478", first.cpf()),
            () -> assertEquals("MARIA MARTINS", first.fullName()),
            () -> assertEquals(19460612, first.birthDate()),
            () -> assertEquals(28566181479L, first.nis()),
            () -> assertEquals("02", first.regionCode()),
            () -> assertEquals("PBF1", first.programCode()),
            () -> assertEquals("A", first.status()),
            () -> assertEquals(new BigDecimal("1000.00"), first.familyIncome()),
            () -> assertEquals(0, first.dependentCount()),
            () -> assertEquals("S", first.docsOk()));
    }

    @Test
    void should_not_split_a_record_on_a_carriage_return_inside_a_packed_field() throws IOException {
        // Um valor negativo terminado no dígito 0 grava 0x0D no último byte, que a
        // leitura por linha trataria como fim de registro e partiria ao meio.
        byte[] withCarriageReturn = record(
            "10000000001", "52998224725", "PESSOA UM", "19800101", "00000000000",
            "01", "PBF1", "A", new byte[] {0x00, 0x01, 0x00, 0x00, 0x0D}, "02", "S");
        byte[] following = record(
            "10000000002", "11144477735", "PESSOA DOIS", "19900202", "00000000000",
            "03", "BPC2", "S", new byte[] {0x00, 0x00, 0x50, 0x00, 0x0C}, "01", "N");

        List<LegacyBeneficiaryRecord> records = read(
            concat(withCarriageReturn, separator(), following, separator()));

        assertAll(
            () -> assertEquals(2, records.size()),
            () -> assertEquals(new BigDecimal("-1000.00"), records.get(0).familyIncome()),
            () -> assertEquals("11144477735", records.get(1).cpf()),
            () -> assertEquals(new BigDecimal("500.00"), records.get(1).familyIncome()),
            () -> assertEquals(2L, records.get(1).lineNumber()));
    }

    @Test
    void should_read_the_last_record_when_the_file_has_no_trailing_separator() throws IOException {
        byte[] record = record(
            "10000000001", "52998224725", "PESSOA UM", "19800101", "00000000000",
            "01", "PBF1", "A", new byte[] {0x00, 0x00, 0x05, 0x00, 0x0C}, "02", "S");

        assertEquals(1, read(record).size());
    }

    @Test
    void should_reject_a_truncated_file_instead_of_loading_a_partial_record() {
        byte[] record = record(
            "10000000001", "52998224725", "PESSOA UM", "19800101", "00000000000",
            "01", "PBF1", "A", new byte[] {0x00, 0x00, 0x05, 0x00, 0x0C}, "02", "S");
        byte[] truncated = new byte[record.length - 10];
        System.arraycopy(record, 0, truncated, 0, truncated.length);

        assertThrows(EOFException.class, () -> read(truncated));
    }

    @Test
    void should_reject_a_file_whose_records_lost_alignment() {
        byte[] record = record(
            "10000000001", "52998224725", "PESSOA UM", "19800101", "00000000000",
            "01", "PBF1", "A", new byte[] {0x00, 0x00, 0x05, 0x00, 0x0C}, "02", "S");

        assertThrows(IOException.class, () -> read(concat(record, "X".getBytes(StandardCharsets.ISO_8859_1))));
    }

    private List<LegacyBeneficiaryRecord> read(byte[] data) throws IOException {
        FixedWidthLayout layout = FixedWidthLayout.parse(
            new ByteArrayInputStream(LAYOUT.getBytes(StandardCharsets.UTF_8)));
        return new LegacyBeneficiaryReader(layout).readAll(new ByteArrayInputStream(data));
    }

    private byte[] record(
        String registration,
        String cpf,
        String name,
        String birthDate,
        String nis,
        String region,
        String program,
        String status,
        byte[] income,
        String dependents,
        String docsOk
    ) {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        out.writeBytes(fixed(registration, 11));
        out.writeBytes(fixed(cpf, 11));
        out.writeBytes(fixed(name, 20));
        out.writeBytes(fixed(birthDate, 8));
        out.writeBytes(fixed(nis, 11));
        out.writeBytes(fixed(region, 2));
        out.writeBytes(fixed(program, 4));
        out.writeBytes(fixed(status, 1));
        out.writeBytes(income);
        out.writeBytes(fixed(dependents, 2));
        out.writeBytes(fixed(docsOk, 1));
        return out.toByteArray();
    }

    private byte[] fixed(String value, int width) {
        String truncated = value.length() > width ? value.substring(0, width) : value;
        byte[] padded = new byte[width];
        java.util.Arrays.fill(padded, (byte) ' ');
        byte[] source = truncated.getBytes(StandardCharsets.ISO_8859_1);
        System.arraycopy(source, 0, padded, 0, source.length);
        return padded;
    }

    private byte[] separator() {
        return new byte[] {'\n'};
    }

    private byte[] concat(byte[]... parts) {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        for (byte[] part : parts) {
            out.writeBytes(part);
        }
        return out.toByteArray();
    }
}
