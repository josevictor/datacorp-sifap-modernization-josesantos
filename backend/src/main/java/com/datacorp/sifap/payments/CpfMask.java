package com.datacorp.sifap.payments;

/**
 * Máscara de exibição do CPF (REQ-037).
 *
 * <p>Espelha a sub-rotina {@code MASK-CPF} de {@code CONSBENF.NSP:292-311},
 * com uma divergência deliberada: o legado tem dois ramos e este tem um só.
 *
 * <p>Quando o CPF armazenado tem menos de onze dígitos, o legado revela os
 * <strong>três primeiros</strong> em vez dos cinco últimos. O próprio código
 * marca o comportamento como {@code KNOWN INCONSISTENCY}. Como as duas
 * máscaras protegem partes diferentes do documento, quem visse ambas as telas
 * reconstruiria a maior parte do CPF.
 *
 * <p>O ramo não é replicado. Ele também é inalcançável nesta base: a coluna é
 * {@code VARCHAR(11)} e a validação exige onze dígitos.
 */
final class CpfMask {

    private CpfMask() {
    }

    /**
     * Formata o CPF como {@code ***.***.XXX-XX}, revelando apenas os cinco
     * últimos dígitos.
     *
     * @param cpf CPF com onze dígitos
     * @return CPF mascarado
     * @throws IllegalArgumentException se o CPF não tiver onze dígitos
     */
    static String of(String cpf) {
        if (cpf == null || !cpf.matches("\\d{11}")) {
            throw new IllegalArgumentException("CPF must have 11 digits to be masked");
        }
        return "***.***." + cpf.substring(6, 9) + "-" + cpf.substring(9, 11);
    }
}
