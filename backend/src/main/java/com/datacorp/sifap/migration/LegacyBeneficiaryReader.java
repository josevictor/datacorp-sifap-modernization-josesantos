package com.datacorp.sifap.migration;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

/**
 * Leitor da extração de beneficiários.
 *
 * <p>Mapeia apenas os campos do escopo de carga — os que o sistema moderno
 * consome — e não os 69 campos do cadastro legado. O enquadramento dos
 * registros fica a cargo de {@link FixedWidthReader}.
 */
public final class LegacyBeneficiaryReader {

    private final FixedWidthReader reader;

    public LegacyBeneficiaryReader(FixedWidthLayout layout) {
        this.reader = new FixedWidthReader(layout);
    }

    /**
     * Lê todos os registros da extração.
     *
     * @param source arquivo {@code beneficiary.dat}; é totalmente consumido
     * @return registros na ordem do arquivo
     * @throws IOException se a leitura falhar ou a extração estiver truncada
     */
    public List<LegacyBeneficiaryRecord> readAll(InputStream source) throws IOException {
        return reader.readAll(source, record -> new LegacyBeneficiaryRecord(
            record.lineNumber(),
            record.text("NUM-REGISTRATION"),
            record.text("NUM-CPF"),
            record.text("FULL-NAME"),
            (int) record.number("DT-BIRTH"),
            record.number("NUM-NIS"),
            record.text("COD-REGION"),
            record.text("COD-PROGRAM"),
            record.text("STAT-BENEFICIARY"),
            record.packed("AMT-FAMILY-INCOME"),
            (int) record.number("QTY-DEPEND"),
            record.text("IND-DOCS-OK")));
    }
}
