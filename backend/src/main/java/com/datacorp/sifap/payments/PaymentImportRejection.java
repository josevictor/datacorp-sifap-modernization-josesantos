package com.datacorp.sifap.payments;

/**
 * Motivo pelo qual um pagamento legado não pôde ser carregado.
 */
public enum PaymentImportRejection {

    /** {@code NUM-CPF} não passa na validação dos dígitos verificadores. */
    INVALID_CPF,

    /** Não existe beneficiário carregado para o {@code NUM-CPF} do pagamento. */
    UNKNOWN_BENEFICIARY,

    /** {@code YEAR-MONTH-REF} não é um período {@code AAAAMM} válido. */
    INVALID_PERIOD,

    /** {@code DT-GENERATION} não é uma data de calendário válida. */
    INVALID_GENERATION_DATE,

    /** {@code COD-PROGRAM} está em branco. */
    EMPTY_PROGRAM,

    /** {@code STAT-PAYMENT} está fora do domínio do DDM. */
    INVALID_STATUS,

    /** {@code TYPE-PAYMENT} está fora do domínio do DDM. */
    INVALID_PAYMENT_TYPE,

    /** Algum valor monetário é negativo. */
    NEGATIVE_AMOUNT,

    /** O mesmo par CPF e período de referência aparece mais de uma vez na extração. */
    DUPLICATE_PERIOD_IN_FILE,

    /** {@code AMT-DISC-TOTAL} excede a precisão {@code NUMERIC(7,2)} da coluna. */
    DISCOUNT_OUT_OF_RANGE
}
