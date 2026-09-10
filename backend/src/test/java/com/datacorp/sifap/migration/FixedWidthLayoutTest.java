package com.datacorp.sifap.migration;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import org.junit.jupiter.api.Test;

class FixedWidthLayoutTest {

    @Test
    void should_derive_offsets_by_accumulating_declared_widths() throws IOException {
        String layout = """
            # LEVEL CODE NAME FORMAT LENGTH OCCURS OPTIONS BYTE-WIDTH
            01 AA NUM-REGISTRATION  N 11   1  DE,UQ  11
            01 AB NUM-CPF           A 11   1  DE     11
            01 CH AMT-FAMILY-INCOME P 9,2  1  -      5
            """;

        FixedWidthLayout parsed = FixedWidthLayout.parse(stream(layout));

        assertAll(
            () -> assertEquals(0, parsed.field("NUM-REGISTRATION").offset()),
            () -> assertEquals(11, parsed.field("NUM-CPF").offset()),
            () -> assertEquals(22, parsed.field("AMT-FAMILY-INCOME").offset()),
            () -> assertEquals(5, parsed.field("AMT-FAMILY-INCOME").width()),
            () -> assertEquals(2, parsed.field("AMT-FAMILY-INCOME").scale()),
            () -> assertEquals(27, parsed.recordWidth()));
    }

    @Test
    void should_divide_the_declared_width_across_occurrences_of_a_repeating_field() throws IOException {
        String layout = """
            02 DB CPF-DEPEND A 11 10 - 110
            """;

        FixedWidthLayout.LayoutField field = FixedWidthLayout.parse(stream(layout)).field("CPF-DEPEND");

        assertAll(
            () -> assertEquals(11, field.width()),
            () -> assertEquals(10, field.occurs()));
    }

    @Test
    void should_reject_a_layout_whose_widths_disagree_with_the_declared_total() {
        String layout = """
            01 AA NUM-REGISTRATION N 11 1 DE 11
            # RECORD-BYTES 99
            """;

        IllegalArgumentException failure = assertThrows(
            IllegalArgumentException.class,
            () -> FixedWidthLayout.parse(stream(layout)));

        assertTrue(failure.getMessage().contains("RECORD-BYTES"));
    }

    @Test
    void should_reject_an_unknown_field_rather_than_returning_a_default_position() throws IOException {
        FixedWidthLayout parsed = FixedWidthLayout.parse(stream("01 AA NUM-REGISTRATION N 11 1 DE 11\n"));

        assertThrows(IllegalArgumentException.class, () -> parsed.field("NAO-EXISTE"));
    }

    @Test
    void should_position_the_migrated_fields_of_the_real_legacy_layout() throws IOException {
        // Blindagem contra deslocamento: um offset errado não falha, apenas lê o
        // campo vizinho e devolve um valor plausível.
        try (InputStream source = Files.newInputStream(LegacySeedData.file("layout-beneficiary.txt"))) {
            FixedWidthLayout parsed = FixedWidthLayout.parse(source);

            assertAll(
                () -> assertEquals(1739, parsed.recordWidth()),
                () -> assertEquals(0, parsed.field("NUM-REGISTRATION").offset()),
                () -> assertEquals(11, parsed.field("NUM-CPF").offset()),
                () -> assertEquals(22, parsed.field("FULL-NAME").offset()),
                () -> assertEquals(202, parsed.field("DT-BIRTH").offset()),
                () -> assertEquals(247, parsed.field("NUM-NIS").offset()),
                () -> assertEquals(451, parsed.field("UF").offset()),
                () -> assertEquals(468, parsed.field("COD-REGION").offset()),
                () -> assertEquals(470, parsed.field("COD-PROGRAM").offset()),
                () -> assertEquals(498, parsed.field("STAT-BENEFICIARY").offset()),
                () -> assertEquals(510, parsed.field("AMT-FAMILY-INCOME").offset()),
                () -> assertEquals(5, parsed.field("AMT-FAMILY-INCOME").width()),
                () -> assertEquals(521, parsed.field("QTY-DEPEND").offset()),
                () -> assertEquals(523, parsed.field("IND-DOCS-OK").offset()));
        }
    }

    private InputStream stream(String content) {
        return new ByteArrayInputStream(content.getBytes(StandardCharsets.UTF_8));
    }
}
