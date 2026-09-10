package com.datacorp.sifap.migration;

import java.math.BigDecimal;

/**
 * Pagamento lido da extração legada, ainda sem validação.
 *
 * <p>Contém apenas os campos que a tabela {@code payment} do sistema moderno
 * representa. O cadastro legado guarda muito mais — integração SIAFI,
 * conciliação bancária, estorno e a estrutura periódica de descontos —, que
 * permanece fora do escopo de carga.
 *
 * @param lineNumber posição do registro no arquivo, em base 1
 * @param paymentNumber {@code NUM-PAYMENT}, identificador legado
 * @param cpf {@code NUM-CPF} do beneficiário
 * @param programCode {@code COD-PROGRAM}
 * @param referencePeriod {@code YEAR-MONTH-REF} no formato {@code AAAAMM}
 * @param grossAmount {@code AMT-GROSS}
 * @param discountTotal {@code AMT-DISC-TOTAL}
 * @param netAmount {@code AMT-NET}
 * @param bonusAmount {@code AMT-BONUS}
 * @param generationDate {@code DT-GENERATION} no formato {@code AAAAMMDD}
 * @param status {@code STAT-PAYMENT}
 * @param paymentType {@code TYPE-PAYMENT}
 */
public record LegacyPaymentRecord(
    long lineNumber,
    long paymentNumber,
    String cpf,
    String programCode,
    int referencePeriod,
    BigDecimal grossAmount,
    BigDecimal discountTotal,
    BigDecimal netAmount,
    BigDecimal bonusAmount,
    int generationDate,
    String status,
    String paymentType
) {
}
