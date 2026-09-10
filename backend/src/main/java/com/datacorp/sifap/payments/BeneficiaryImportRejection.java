package com.datacorp.sifap.payments;

/**
 * Motivo pelo qual um registro legado não pôde ser carregado.
 *
 * <p>Cada registro recusado é reportado com seu motivo em vez de ser
 * descartado em silêncio: uma carga que "funciona" perdendo registros sem
 * aviso é pior do que uma carga que falha.
 */
public enum BeneficiaryImportRejection {

    /** {@code NUM-CPF} não passa na validação dos dígitos verificadores. */
    INVALID_CPF,

    /** O mesmo {@code NUM-CPF} aparece mais de uma vez na extração. */
    DUPLICATE_CPF_IN_FILE,

    /** {@code FULL-NAME} está em branco. */
    EMPTY_NAME,

    /** {@code DT-BIRTH} não é uma data de calendário válida. */
    INVALID_BIRTH_DATE,

    /** {@code COD-REGION} está fora do domínio com fator de pagamento autorizado. */
    UNKNOWN_REGION,

    /** {@code STAT-BENEFICIARY} está fora do domínio do DDM. */
    INVALID_STATUS,

    /** {@code COD-PROGRAM} está em branco. */
    EMPTY_PROGRAM,

    /** {@code AMT-FAMILY-INCOME} é negativo. */
    NEGATIVE_INCOME,

    /** {@code QTY-DEPEND} é negativo. */
    NEGATIVE_DEPENDENTS,

    /** {@code IND-DOCS-OK} não é {@code S} nem {@code N}. */
    INVALID_DOCS_FLAG,

    /** {@code NUM-NIS} preenchido colide com outro registro, violando {@code DE,UQ,NU}. */
    DUPLICATE_NIS
}
