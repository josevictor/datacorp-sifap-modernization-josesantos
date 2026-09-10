package com.datacorp.sifap.payments;

/**
 * Descrição da situação cadastral do beneficiário (REQ-038).
 *
 * <p>Espelha o {@code DECIDE ON FIRST VALUE OF STAT-BENEFICIARY} de
 * {@code CONSBENF.NSP:228-241}, incluindo o ramo {@code NONE}, que descreve
 * qualquer código fora do conjunto conhecido como desconhecido em vez de
 * falhar.
 */
enum BeneficiaryStatusDescription {

    ACTIVE("A", "Ativo"),
    SUSPENDED("S", "Suspenso"),
    CANCELED("C", "Cancelado"),
    INACTIVE("I", "Inativo"),
    TERMINATED("D", "Encerrado");

    private static final String UNKNOWN = "Desconhecido";

    private final String code;
    private final String description;

    BeneficiaryStatusDescription(String code, String description) {
        this.code = code;
        this.description = description;
    }

    /**
     * Descreve o código de situação armazenado.
     *
     * @param code código de um caractere lido do cadastro
     * @return descrição correspondente, ou {@code Desconhecido}
     */
    static String of(String code) {
        for (BeneficiaryStatusDescription status : values()) {
            if (status.code.equals(code)) {
                return status.description;
            }
        }
        return UNKNOWN;
    }
}
