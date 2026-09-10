package com.datacorp.sifap.payments;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

/**
 * Regras de elegibilidade por tipo de programa, espelhando o
 * {@code DECIDE ON FIRST VALUE OF #TYPE-PROG} de {@code VALELEG.NSN}
 * (REQ-027 a REQ-030).
 *
 * <p>Os limites de idade abaixo são literais fixos no código legado e
 * coexistem com {@code AGE-MIN} e {@code AGE-MAX} do cadastro do programa. As
 * duas verificações são independentes e ambas podem recusar o mesmo
 * beneficiário.
 */
final class ProgramTypeRule {

    private static final BigDecimal ASSISTANCE_INCOME_LIMIT = new BigDecimal("600.00");
    private static final int PENSION_MIN_AGE = 60;
    private static final int EMPLOYMENT_MIN_AGE = 16;
    private static final int EMPLOYMENT_MAX_AGE = 65;

    private ProgramTypeRule() {
    }

    static List<EligibilityReason> evaluate(SocialProgram program, Beneficiary beneficiary, int age) {
        List<EligibilityReason> reasons = new ArrayList<>();
        switch (program.type()) {
            case "A" -> evaluateAssistance(beneficiary, reasons);
            case "P" -> {
                if (age < PENSION_MIN_AGE) {
                    reasons.add(EligibilityReason.PENSION_AGE_BELOW_MINIMUM);
                }
            }
            case "T" -> {
                if (age < EMPLOYMENT_MIN_AGE || age > EMPLOYMENT_MAX_AGE) {
                    reasons.add(EligibilityReason.EMPLOYMENT_AGE_OUT_OF_RANGE);
                }
            }
            default -> reasons.add(EligibilityReason.UNKNOWN_PROGRAM_TYPE);
        }
        return reasons;
    }

    private static void evaluateAssistance(Beneficiary beneficiary, List<EligibilityReason> reasons) {
        // A recusa por renda só ocorre quando não há dependentes: o legado
        // aninha a verificação de dependentes dentro da verificação de renda.
        if (beneficiary.familyIncome().compareTo(ASSISTANCE_INCOME_LIMIT) > 0
            && beneficiary.dependentCount() < 1) {
            reasons.add(EligibilityReason.ASSISTANCE_INCOME_WITHOUT_DEPENDENTS);
        }
        if (!beneficiary.hasCompleteDocumentation()) {
            reasons.add(EligibilityReason.INCOMPLETE_DOCUMENTATION);
        }
    }
}
