package com.datacorp.sifap.payments;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * Validação de elegibilidade, portando {@code VALELEG.NSN} (REQ-020 a REQ-032).
 *
 * <p><strong>A ordem das verificações é comportamento observável.</strong> Três
 * delas encerram a rotina antecipadamente e apenas o primeiro motivo acumulado
 * é devolvido, então reordenar as regras mudaria a resposta ao operador mesmo
 * quando a decisão final permanecesse a mesma.
 *
 * <p>A idade usa o ano do período processado, coerente com
 * {@code PaymentCalculationService}. O legado calcula a idade duas vezes de
 * formas divergentes — {@code BATCHPGT} com a janela de século Y2K e sobre o
 * ano do período, {@code VALELEG} sem a janela e sobre o ano corrente. Essa
 * divergência decorre de um contrato de PDA nunca revisto, não de regra de
 * negócio, e não é replicada. Consulte o achado correspondente em
 * {@code 01-archaeology/mysteries-found.md}.
 */
@Service
class EligibilityValidationService {

    private static final String SPECIAL_REGION = "99";

    EligibilityStatus validate(Beneficiary beneficiary, SocialProgram program, YearMonthPeriod period) {
        // Saída antecipada 1: o programa inativo é avaliado antes de qualquer
        // regra do beneficiário, inclusive antes do desvio da região especial.
        if (!program.isActive()) {
            return EligibilityStatus.terminatedWith(EligibilityReason.PROGRAM_INACTIVE);
        }

        // Saída antecipada 2: ver o comentário de bypassesAllValidations.
        if (bypassesAllValidations(beneficiary)) {
            return EligibilityStatus.eligible();
        }

        int age = period.year() - beneficiary.birthYear();
        List<EligibilityReason> reasons = new ArrayList<>();

        registrationStatusReason(beneficiary).ifPresent(reasons::add);
        reasons.addAll(ageRangeReasons(program, age));
        reasons.addAll(incomeCeilingReasons(program, beneficiary));
        reasons.addAll(ProgramTypeRule.evaluate(program, beneficiary, age));
        reasons.addAll(EligibilityCode.of(program.eligibilityCode()).evaluate(beneficiary));

        return EligibilityStatus.ineligible(reasons);
    }

    /**
     * REQ-023 — a região {@code 99} declara o beneficiário elegível e encerra a
     * validação, dispensando situação cadastral, faixa etária, teto de renda,
     * regras por tipo de programa e código de elegibilidade.
     *
     * <p>Nenhuma regra de negócio localizada autoriza este desvio; o comentário
     * legado apenas o rotula como internacional/diplomático, e a documentação
     * de 2012 registra que sua origem nunca foi explicada. O comportamento é
     * preservado por fidelidade e isolado neste método para que a remoção
     * futura seja pontual. Questão aberta {@code SIFAP-M-12}.
     */
    private boolean bypassesAllValidations(Beneficiary beneficiary) {
        return SPECIAL_REGION.equals(beneficiary.regionCode());
    }

    private java.util.Optional<EligibilityReason> registrationStatusReason(Beneficiary beneficiary) {
        // O legado não tem ramo final: uma situação fora destas quatro não
        // gera motivo e o beneficiário permanece elegível.
        return switch (beneficiary.status()) {
            case "S" -> java.util.Optional.of(EligibilityReason.BENEFICIARY_SUSPENDED);
            case "C", "D" -> java.util.Optional.of(EligibilityReason.BENEFICIARY_CANCELED_OR_REMOVED);
            case "I" -> java.util.Optional.of(EligibilityReason.BENEFICIARY_INACTIVE);
            default -> java.util.Optional.empty();
        };
    }

    /** Zero desativa o limite, conforme {@code IF #AGE-MIN > 0}. */
    private List<EligibilityReason> ageRangeReasons(SocialProgram program, int age) {
        List<EligibilityReason> reasons = new ArrayList<>();
        if (program.ageMin() > 0 && age < program.ageMin()) {
            reasons.add(EligibilityReason.AGE_BELOW_PROGRAM_MINIMUM);
        }
        if (program.ageMax() > 0 && age > program.ageMax()) {
            reasons.add(EligibilityReason.AGE_ABOVE_PROGRAM_MAXIMUM);
        }
        return reasons;
    }

    /**
     * O campo legado se chama {@code MAX-PERCAP-INCOME}, mas a comparação usa a
     * renda familiar declarada, não a renda per capita. A divergência é
     * preservada deliberadamente: corrigi-la mudaria quem recebe benefício.
     */
    private List<EligibilityReason> incomeCeilingReasons(SocialProgram program, Beneficiary beneficiary) {
        BigDecimal ceiling = program.maxIncome();
        if (ceiling.compareTo(BigDecimal.ZERO) > 0
            && beneficiary.familyIncome().compareTo(ceiling) > 0) {
            return List.of(EligibilityReason.FAMILY_INCOME_ABOVE_PROGRAM_CEILING);
        }
        return List.of();
    }
}
