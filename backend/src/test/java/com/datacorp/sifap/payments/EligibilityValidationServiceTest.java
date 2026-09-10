package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.math.BigDecimal;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class EligibilityValidationServiceTest {

    private static final YearMonthPeriod PERIOD = YearMonthPeriod.of(202609);

    private final EligibilityValidationService service = new EligibilityValidationService();

    // ---------------------------------------------------------------
    // Saídas antecipadas
    // ---------------------------------------------------------------

    @Test
    void should_terminate_with_program_inactive_when_program_is_not_active() {
        // REQ-022
        EligibilityStatus status = service.validate(
            beneficiary().status("A").build(),
            program().status("I").build(),
            PERIOD);

        assertAll(
            () -> assertFalse(status.isEligible()),
            () -> assertEquals(2004, status.returnCode()),
            () -> assertEquals(EligibilityReason.PROGRAM_INACTIVE, status.reason().orElseThrow())
        );
    }

    @Test
    void should_prefer_program_inactive_over_beneficiary_rules() {
        // REQ-022 — o programa é avaliado antes de qualquer regra do beneficiário.
        EligibilityStatus status = service.validate(
            beneficiary().status("S").build(),
            program().status("I").build(),
            PERIOD);

        assertEquals(EligibilityReason.PROGRAM_INACTIVE, status.reason().orElseThrow());
    }

    // ---------------------------------------------------------------
    // Região 99 — comportamento preservado, questão SIFAP-M-12
    // ---------------------------------------------------------------

    @Test
    void should_bypass_all_validations_when_region_is_special() {
        // REQ-023 / AC-023.1 — beneficiário suspenso, fora da faixa etária,
        // acima do teto de renda e sem documentação permanece elegível.
        EligibilityStatus status = service.validate(
            beneficiary()
                .region("99")
                .status("S")
                .income("99999.00")
                .docsOk("N")
                .build(),
            program().type("P").ageMin((short) 18).maxIncome("100.00").build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    @Test
    void should_prefer_program_inactive_over_special_region() {
        // REQ-023 / AC-023.2 — o desvio ocorre depois da checagem do programa.
        EligibilityStatus status = service.validate(
            beneficiary().region("99").build(),
            program().status("I").build(),
            PERIOD);

        assertEquals(EligibilityReason.PROGRAM_INACTIVE, status.reason().orElseThrow());
    }

    @Test
    void should_evaluate_all_rules_when_region_is_not_special() {
        // REQ-023 / AC-023.3
        EligibilityStatus status = service.validate(
            beneficiary().region("01").status("S").build(),
            program().build(),
            PERIOD);

        assertFalse(status.isEligible());
    }

    // ---------------------------------------------------------------
    // Situação cadastral
    // ---------------------------------------------------------------

    @Test
    void should_reject_suspended_beneficiary() {
        // REQ-024 / AC-024.1
        EligibilityStatus status = service.validate(
            beneficiary().status("S").build(), program().build(), PERIOD);

        assertEquals(EligibilityReason.BENEFICIARY_SUSPENDED, status.reason().orElseThrow());
    }

    @Test
    void should_reject_canceled_or_removed_beneficiary() {
        // REQ-024 / AC-024.2
        assertAll(
            () -> assertEquals(
                EligibilityReason.BENEFICIARY_CANCELED_OR_REMOVED,
                service.validate(beneficiary().status("C").build(), program().build(), PERIOD)
                    .reason().orElseThrow()),
            () -> assertEquals(
                EligibilityReason.BENEFICIARY_CANCELED_OR_REMOVED,
                service.validate(beneficiary().status("D").build(), program().build(), PERIOD)
                    .reason().orElseThrow())
        );
    }

    @Test
    void should_accept_active_beneficiary_without_status_reason() {
        // REQ-024 / AC-024.3
        EligibilityStatus status = service.validate(
            beneficiary().status("A").build(), program().build(), PERIOD);

        assertTrue(status.isEligible());
    }

    @Test
    void should_keep_beneficiary_eligible_when_status_is_unknown() {
        // REQ-024 — o IF aninhado do legado não tem ramo final: uma situação
        // fora de A, S, C, D e I não gera motivo. Comportamento preservado.
        EligibilityStatus status = service.validate(
            beneficiary().status("Z").build(), program().build(), PERIOD);

        assertTrue(status.isEligible());
    }

    // ---------------------------------------------------------------
    // Faixa etária do programa
    // ---------------------------------------------------------------

    @Test
    void should_reject_age_below_program_minimum() {
        // REQ-025 / AC-025.1 — nascido em 2010, 16 anos no período de 2026.
        EligibilityStatus status = service.validate(
            beneficiary().birthDate(20100101).build(),
            program().ageMin((short) 18).build(),
            PERIOD);

        assertEquals(EligibilityReason.AGE_BELOW_PROGRAM_MINIMUM, status.reason().orElseThrow());
    }

    @Test
    void should_ignore_age_minimum_when_it_is_zero() {
        // REQ-025 / AC-025.2
        EligibilityStatus status = service.validate(
            beneficiary().birthDate(20100101).build(),
            program().ageMin((short) 0).build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    @Test
    void should_accept_age_equal_to_program_maximum() {
        // REQ-025 / AC-025.3 — limite inclusivo: 65 anos com máximo 65.
        EligibilityStatus status = service.validate(
            beneficiary().birthDate(19610101).build(),
            program().ageMax((short) 65).build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    @Test
    void should_reject_age_above_program_maximum() {
        // REQ-025 — 66 anos com máximo 65.
        EligibilityStatus status = service.validate(
            beneficiary().birthDate(19600101).build(),
            program().ageMax((short) 65).build(),
            PERIOD);

        assertEquals(EligibilityReason.AGE_ABOVE_PROGRAM_MAXIMUM, status.reason().orElseThrow());
    }

    // ---------------------------------------------------------------
    // Teto de renda
    // ---------------------------------------------------------------

    @Test
    void should_reject_income_above_program_ceiling() {
        // REQ-026 / AC-026.1
        EligibilityStatus status = service.validate(
            beneficiary().income("1000.01").build(),
            program().maxIncome("1000.00").build(),
            PERIOD);

        assertEquals(
            EligibilityReason.FAMILY_INCOME_ABOVE_PROGRAM_CEILING, status.reason().orElseThrow());
    }

    @Test
    void should_accept_income_equal_to_program_ceiling() {
        // REQ-026 / AC-026.2 — limite inclusivo.
        EligibilityStatus status = service.validate(
            beneficiary().income("1000.00").build(),
            program().maxIncome("1000.00").build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    @Test
    void should_ignore_income_ceiling_when_it_is_zero() {
        // REQ-026 / AC-026.3
        EligibilityStatus status = service.validate(
            beneficiary().income("99999.00").build(),
            program().maxIncome("0.00").build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    // ---------------------------------------------------------------
    // Regras por tipo de programa
    // ---------------------------------------------------------------

    @Test
    void should_reject_assistance_program_when_documentation_is_incomplete() {
        // REQ-027 / AC-027.1
        EligibilityStatus status = service.validate(
            beneficiary().docsOk("N").build(),
            program().type("A").build(),
            PERIOD);

        assertEquals(EligibilityReason.INCOMPLETE_DOCUMENTATION, status.reason().orElseThrow());
    }

    @Test
    void should_reject_assistance_program_when_income_is_high_without_dependents() {
        // REQ-027 / AC-027.2
        EligibilityStatus status = service.validate(
            beneficiary().income("700.00").dependents(0).build(),
            program().type("A").build(),
            PERIOD);

        assertEquals(
            EligibilityReason.ASSISTANCE_INCOME_WITHOUT_DEPENDENTS, status.reason().orElseThrow());
    }

    @Test
    void should_accept_assistance_program_when_income_is_high_with_dependents() {
        // REQ-027 / AC-027.3 — a recusa por renda é aninhada na ausência de
        // dependentes, então um dependente basta para afastá-la.
        EligibilityStatus status = service.validate(
            beneficiary().income("700.00").dependents(1).build(),
            program().type("A").build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    @Test
    void should_reject_pension_program_below_minimum_age() {
        // REQ-028 / AC-028.1 — 59 anos.
        EligibilityStatus status = service.validate(
            beneficiary().birthDate(19670101).build(),
            program().type("P").build(),
            PERIOD);

        assertEquals(EligibilityReason.PENSION_AGE_BELOW_MINIMUM, status.reason().orElseThrow());
    }

    @Test
    void should_accept_pension_program_at_minimum_age() {
        // REQ-028 / AC-028.2 — 60 anos.
        EligibilityStatus status = service.validate(
            beneficiary().birthDate(19660101).build(),
            program().type("P").build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    @Test
    void should_reject_employment_program_outside_age_range() {
        // REQ-029 / AC-029.1 e AC-029.2 — 15 anos e 66 anos.
        assertAll(
            () -> assertEquals(
                EligibilityReason.EMPLOYMENT_AGE_OUT_OF_RANGE,
                service.validate(
                        beneficiary().birthDate(20110101).build(),
                        program().type("T").build(),
                        PERIOD)
                    .reason().orElseThrow()),
            () -> assertEquals(
                EligibilityReason.EMPLOYMENT_AGE_OUT_OF_RANGE,
                service.validate(
                        beneficiary().birthDate(19600101).build(),
                        program().type("T").build(),
                        PERIOD)
                    .reason().orElseThrow())
        );
    }

    @Test
    void should_accept_employment_program_inside_age_range() {
        // REQ-029 / AC-029.3 — 46 anos.
        EligibilityStatus status = service.validate(
            beneficiary().birthDate(19800101).build(),
            program().type("T").build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    @Test
    void should_reject_unknown_program_type() {
        // REQ-030 / AC-030.1 e AC-030.2 — beneficiário sem nenhuma outra
        // violação continua inelegível.
        EligibilityStatus status = service.validate(
            beneficiary().build(),
            program().type("X").build(),
            PERIOD);

        assertAll(
            () -> assertFalse(status.isEligible()),
            () -> assertEquals(EligibilityReason.UNKNOWN_PROGRAM_TYPE, status.reason().orElseThrow())
        );
    }

    // ---------------------------------------------------------------
    // Código de elegibilidade
    // ---------------------------------------------------------------

    @Test
    void should_reject_when_eligibility_code_requires_nis_and_nis_is_absent() {
        // REQ-031 / AC-031.1
        EligibilityStatus status = service.validate(
            beneficiary().nis(0L).build(),
            program().eligibilityCode("R    ").build(),
            PERIOD);

        assertEquals(EligibilityReason.NIS_NOT_REGISTERED, status.reason().orElseThrow());
    }

    @Test
    void should_reject_when_eligibility_code_requires_dependents_and_none_exist() {
        // REQ-031 / AC-031.2
        EligibilityStatus status = service.validate(
            beneficiary().dependents(0).build(),
            program().eligibilityCode(" D   ").build(),
            PERIOD);

        assertEquals(EligibilityReason.PROGRAM_REQUIRES_DEPENDENTS, status.reason().orElseThrow());
    }

    @Test
    void should_ignore_eligibility_code_when_it_is_blank() {
        // REQ-031 / AC-031.3
        EligibilityStatus status = service.validate(
            beneficiary().nis(0L).dependents(0).build(),
            program().eligibilityCode("").build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    @Test
    void should_ignore_positions_three_to_five_of_eligibility_code() {
        // REQ-031 / AC-031.4 — o legado só lê as posições 1 e 2 por SUBSTR.
        EligibilityStatus status = service.validate(
            beneficiary().nis(0L).dependents(0).build(),
            program().eligibilityCode("  RDX").build(),
            PERIOD);

        assertTrue(status.isEligible());
    }

    // ---------------------------------------------------------------
    // Precedência do motivo devolvido
    // ---------------------------------------------------------------

    @Test
    void should_return_first_reason_when_multiple_rules_are_violated() {
        // REQ-032 / AC-032.2 — situação cadastral é avaliada antes da idade.
        EligibilityStatus status = service.validate(
            beneficiary().status("S").birthDate(20100101).build(),
            program().ageMin((short) 18).build(),
            PERIOD);

        assertAll(
            () -> assertEquals(2010, status.returnCode()),
            () -> assertEquals(EligibilityReason.BENEFICIARY_SUSPENDED, status.reason().orElseThrow()),
            () -> assertEquals(2, status.allReasons().size())
        );
    }

    @Test
    void should_return_zero_code_and_no_reason_when_eligible() {
        // REQ-032 / AC-032.3
        EligibilityStatus status = service.validate(
            beneficiary().build(), program().build(), PERIOD);

        assertAll(
            () -> assertTrue(status.isEligible()),
            () -> assertEquals(0, status.returnCode()),
            () -> assertTrue(status.reason().isEmpty())
        );
    }

    // ---------------------------------------------------------------
    // Builders
    // ---------------------------------------------------------------

    private BeneficiaryBuilder beneficiary() {
        return new BeneficiaryBuilder();
    }

    private ProgramBuilder program() {
        return new ProgramBuilder();
    }

    private static final class BeneficiaryBuilder {
        private int birthDate = 19800101;
        private String status = "A";
        private String income = "100.00";
        private int dependents = 0;
        private String region = "01";
        private long nis = 1L;
        private String docsOk = "S";

        BeneficiaryBuilder birthDate(int value) {
            this.birthDate = value;
            return this;
        }

        BeneficiaryBuilder status(String value) {
            this.status = value;
            return this;
        }

        BeneficiaryBuilder income(String value) {
            this.income = value;
            return this;
        }

        BeneficiaryBuilder dependents(int value) {
            this.dependents = value;
            return this;
        }

        BeneficiaryBuilder region(String value) {
            this.region = value;
            return this;
        }

        BeneficiaryBuilder nis(long value) {
            this.nis = value;
            return this;
        }

        BeneficiaryBuilder docsOk(String value) {
            this.docsOk = value;
            return this;
        }

        Beneficiary build() {
            return new Beneficiary(
                UUID.randomUUID(), "52998224725", "Pessoa Beneficiaria", birthDate, status,
                "P001", new BigDecimal(income), dependents, region, nis, docsOk);
        }
    }

    private static final class ProgramBuilder {
        private String type = "T";
        private String status = "A";
        private String eligibilityCode = "";
        private short ageMin = 0;
        private short ageMax = 0;
        private String maxIncome = "0.00";

        ProgramBuilder type(String value) {
            this.type = value;
            return this;
        }

        ProgramBuilder status(String value) {
            this.status = value;
            return this;
        }

        ProgramBuilder eligibilityCode(String value) {
            this.eligibilityCode = value;
            return this;
        }

        ProgramBuilder ageMin(short value) {
            this.ageMin = value;
            return this;
        }

        ProgramBuilder ageMax(short value) {
            this.ageMax = value;
            return this;
        }

        ProgramBuilder maxIncome(String value) {
            this.maxIncome = value;
            return this;
        }

        SocialProgram build() {
            return new SocialProgram(
                UUID.randomUUID(), "P001", type, new BigDecimal("100.00"), BigDecimal.ZERO,
                status, eligibilityCode, ageMin, ageMax, new BigDecimal(maxIncome));
        }
    }
}
