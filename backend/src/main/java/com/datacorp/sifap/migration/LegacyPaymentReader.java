package com.datacorp.sifap.migration;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

/**
 * Leitor da extração de pagamentos.
 *
 * <p>Mapeia os campos representados pela tabela {@code payment}; os blocos de
 * integração SIAFI, conciliação e descontos periódicos ficam fora do escopo.
 */
public final class LegacyPaymentReader {

    private final FixedWidthReader reader;

    public LegacyPaymentReader(FixedWidthLayout layout) {
        this.reader = new FixedWidthReader(layout);
    }

    /**
     * Lê todos os registros da extração.
     *
     * @param source arquivo {@code payment.dat}; é totalmente consumido
     * @return registros na ordem do arquivo
     * @throws IOException se a leitura falhar ou a extração estiver truncada
     */
    public List<LegacyPaymentRecord> readAll(InputStream source) throws IOException {
        return reader.readAll(source, record -> new LegacyPaymentRecord(
            record.lineNumber(),
            record.number("NUM-PAYMENT"),
            record.text("NUM-CPF"),
            record.text("COD-PROGRAM"),
            (int) record.number("YEAR-MONTH-REF"),
            record.packed("AMT-GROSS"),
            record.packed("AMT-DISC-TOTAL"),
            record.packed("AMT-NET"),
            record.packed("AMT-BONUS"),
            (int) record.number("DT-GENERATION"),
            record.text("STAT-PAYMENT"),
            record.text("TYPE-PAYMENT")));
    }
}
