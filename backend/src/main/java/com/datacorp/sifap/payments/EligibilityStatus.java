package com.datacorp.sifap.payments;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

/**
 * Resultado da validação de elegibilidade.
 *
 * <p>O legado acumula até dez motivos em {@code #REASON}, mas devolve apenas o
 * primeiro em {@code #PC-MSG} (REQ-032). Preservamos os dois comportamentos: a
 * lista completa fica disponível para diagnóstico, e {@link #reason()} expõe
 * somente o primeiro, que é o valor observável no legado.
 */
final class EligibilityStatus {

    private static final int ELIGIBLE_CODE = 0;
    private static final int INELIGIBLE_CODE = 2010;

    private final int returnCode;
    private final List<EligibilityReason> reasons;

    private EligibilityStatus(int returnCode, List<EligibilityReason> reasons) {
        this.returnCode = returnCode;
        this.reasons = Collections.unmodifiableList(reasons);
    }

    static EligibilityStatus eligible() {
        return new EligibilityStatus(ELIGIBLE_CODE, List.of());
    }

    /** Saída antecipada: encerra a validação sem avaliar as regras seguintes. */
    static EligibilityStatus terminatedWith(EligibilityReason reason) {
        return new EligibilityStatus(reason.returnCode(), List.of(reason));
    }

    static EligibilityStatus ineligible(List<EligibilityReason> reasons) {
        if (reasons.isEmpty()) {
            return eligible();
        }
        return new EligibilityStatus(INELIGIBLE_CODE, new ArrayList<>(reasons));
    }

    boolean isEligible() {
        return returnCode == ELIGIBLE_CODE;
    }

    int returnCode() {
        return returnCode;
    }

    Optional<EligibilityReason> reason() {
        return reasons.isEmpty() ? Optional.empty() : Optional.of(reasons.get(0));
    }

    List<EligibilityReason> allReasons() {
        return reasons;
    }
}
