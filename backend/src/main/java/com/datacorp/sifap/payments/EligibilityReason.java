package com.datacorp.sifap.payments;

/**
 * Motivos de recusa de elegibilidade, espelhando as mensagens de
 * {@code VALELEG.NSN}. A ordem de declaração reproduz a ordem de avaliação do
 * legado, que determina qual motivo é devolvido quando há mais de uma
 * violação (REQ-032).
 */
enum EligibilityReason {

    BENEFICIARY_NOT_FOUND(2001),
    PROGRAM_NOT_FOUND(2003),
    PROGRAM_INACTIVE(2004),
    BENEFICIARY_SUSPENDED(2010),
    BENEFICIARY_CANCELED_OR_REMOVED(2010),
    BENEFICIARY_INACTIVE(2010),
    AGE_BELOW_PROGRAM_MINIMUM(2010),
    AGE_ABOVE_PROGRAM_MAXIMUM(2010),
    FAMILY_INCOME_ABOVE_PROGRAM_CEILING(2010),
    ASSISTANCE_INCOME_WITHOUT_DEPENDENTS(2010),
    INCOMPLETE_DOCUMENTATION(2010),
    PENSION_AGE_BELOW_MINIMUM(2010),
    EMPLOYMENT_AGE_OUT_OF_RANGE(2010),
    UNKNOWN_PROGRAM_TYPE(2010),
    NIS_NOT_REGISTERED(2010),
    PROGRAM_REQUIRES_DEPENDENTS(2010);

    private final int returnCode;

    EligibilityReason(int returnCode) {
        this.returnCode = returnCode;
    }

    int returnCode() {
        return returnCode;
    }
}
