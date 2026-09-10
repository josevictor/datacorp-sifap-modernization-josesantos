package com.datacorp.sifap.payments;

import java.util.List;

/**
 * Código de elegibilidade do programa, campo {@code COD-ELIGIBILITY} de cinco
 * caracteres (REQ-031).
 *
 * <p>O legado interpreta apenas duas posições, por {@code SUBSTR}: a primeira,
 * quando é {@code R}, exige NIS cadastrado; a segunda, quando é {@code D},
 * exige ao menos um dependente. As posições 3 a 5 existem no campo e nunca são
 * lidas — comportamento preservado deliberadamente.
 */
final class EligibilityCode {

    private static final char REQUIRES_NIS = 'R';
    private static final char REQUIRES_DEPENDENTS = 'D';

    private final String value;

    private EligibilityCode(String value) {
        this.value = value;
    }

    static EligibilityCode of(String value) {
        return new EligibilityCode(value == null ? "" : value);
    }

    /**
     * O legado só executa a sub-rotina quando o campo é diferente de branco,
     * conforme {@code IF #COD-ELIG NE ' '}.
     */
    boolean isAbsent() {
        return value.isBlank();
    }

    List<EligibilityReason> evaluate(Beneficiary beneficiary) {
        if (isAbsent()) {
            return List.of();
        }

        List<EligibilityReason> reasons = new java.util.ArrayList<>();
        if (charAt(0) == REQUIRES_NIS && beneficiary.nis() == 0L) {
            reasons.add(EligibilityReason.NIS_NOT_REGISTERED);
        }
        if (charAt(1) == REQUIRES_DEPENDENTS && beneficiary.dependentCount() == 0) {
            reasons.add(EligibilityReason.PROGRAM_REQUIRES_DEPENDENTS);
        }
        return reasons;
    }

    private char charAt(int index) {
        return index < value.length() ? value.charAt(index) : ' ';
    }
}
