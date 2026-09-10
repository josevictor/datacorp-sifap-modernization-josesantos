package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Transactional
class PaymentGenerationIntegrationTest {

    @Autowired
    private BeneficiaryRepository beneficiaryRepository;

    @Autowired
    private SocialProgramRepository socialProgramRepository;

    @Autowired
    private PaymentRepository paymentRepository;

    @Autowired
    private PaymentRejectionRepository paymentRejectionRepository;

    @Autowired
    private PaymentGenerationService paymentGenerationService;

    @Test
    void should_persist_generated_payment_when_beneficiary_is_active_and_period_has_no_payment() {
        // REQ-002, REQ-004, REQ-009
        beneficiaryRepository.save(activeBeneficiary("52998224725", "P001"));
        socialProgramRepository.save(activeProgram("P001"));

        PaymentGenerationResponse response = paymentGenerationService.generate(
            new PaymentGenerationController.PaymentGenerationRequest("52998224725", 202609));

        assertAll(
            () -> assertEquals("GENERATED", response.outcome()),
            () -> assertEquals("G", response.status()),
            () -> assertNotNull(response.paymentId()),
            () -> assertEquals(1, paymentRepository.count())
        );
    }

    @Test
    void should_ignore_generation_when_payment_already_exists_for_cpf_and_period() {
        // REQ-004
        beneficiaryRepository.save(activeBeneficiary("11144477735", "P002"));
        socialProgramRepository.save(activeProgram("P002"));
        paymentGenerationService.generate(new PaymentGenerationController.PaymentGenerationRequest("11144477735", 202609));

        PaymentGenerationResponse response = paymentGenerationService.generate(
            new PaymentGenerationController.PaymentGenerationRequest("11144477735", 202609));

        assertAll(
            () -> assertEquals("IGNORED", response.outcome()),
            () -> assertEquals("PAYMENT_ALREADY_GENERATED", response.reason()),
            () -> assertEquals(1, paymentRepository.count())
        );
    }

    @Test
    void should_ignore_generation_when_beneficiary_is_not_active() {
        // REQ-002
        beneficiaryRepository.save(new Beneficiary(
            UUID.randomUUID(), "11144477735", "Pessoa Inativa", 19800101, "S", "P003",
            new BigDecimal("100.00"), 0, "15"));

        PaymentGenerationResponse response = paymentGenerationService.generate(
            new PaymentGenerationController.PaymentGenerationRequest("11144477735", 202609));

        assertAll(
            () -> assertEquals("IGNORED", response.outcome()),
            () -> assertEquals("BENEFICIARY_NOT_ACTIVE", response.reason()),
            () -> assertEquals(0, paymentRepository.count())
        );
    }

    @Test
    void should_record_rejection_when_cpf_is_invalid() {
        // REQ-003
        PaymentGenerationResponse response = paymentGenerationService.generate(
            new PaymentGenerationController.PaymentGenerationRequest("52998224724", 202609));

        assertAll(
            () -> assertEquals("REJECTED", response.outcome()),
            () -> assertEquals("INVALID_CPF", response.reason()),
            () -> assertEquals(0, paymentRepository.count()),
            () -> assertEquals(1, paymentRejectionRepository.count())
        );
    }

    @Test
    void should_fail_when_beneficiary_does_not_exist() {
        // REQ-020 — equivalente moderno do código 2001 de VALELEG. A busca é
        // resolvida antes da validação de elegibilidade, então o recurso
        // inexistente encerra o fluxo sem avaliar nenhuma regra de programa.
        assertThrows(
            PaymentGenerationNotFoundException.class,
            () -> paymentGenerationService.generate(
                new PaymentGenerationController.PaymentGenerationRequest("39053344705", 202609)));
    }

    @Test
    void should_fail_when_program_does_not_exist() {
        // REQ-021 — equivalente moderno do código 2003. O beneficiário existe,
        // então a falha é do programa, não do cadastro.
        beneficiaryRepository.save(activeBeneficiary("39053344705", "P999"));

        assertThrows(
            PaymentGenerationNotFoundException.class,
            () -> paymentGenerationService.generate(
                new PaymentGenerationController.PaymentGenerationRequest("39053344705", 202609)));
    }

    private Beneficiary activeBeneficiary(String cpf, String programCode) {
        return new Beneficiary(
            UUID.randomUUID(), cpf, "Pessoa Beneficiaria", 19800101, "A", programCode,
            new BigDecimal("100.00"), 0, "15");
    }

    private SocialProgram activeProgram(String code) {
        // Tipo 'A' com documentação completa e renda abaixo de 600,00: o
        // beneficiário do fixture tem 46 anos no período testado e o tipo 'P'
        // exigiria 60 anos (REQ-028), o que tornaria estes casos inelegíveis.
        return new SocialProgram(UUID.randomUUID(), code, "A", new BigDecimal("100.00"), BigDecimal.ZERO, "A");
    }

    @Test
    void should_not_generate_payment_when_beneficiary_is_not_eligible() {
        // REQ-033
        beneficiaryRepository.save(activeBeneficiary("52998224725", "P004"));
        socialProgramRepository.save(new SocialProgram(
            UUID.randomUUID(), "P004", "P", new BigDecimal("100.00"), BigDecimal.ZERO, "A"));

        PaymentGenerationResponse response = paymentGenerationService.generate(
            new PaymentGenerationController.PaymentGenerationRequest("52998224725", 202609));

        assertAll(
            () -> assertEquals("IGNORED", response.outcome()),
            () -> assertEquals("PENSION_AGE_BELOW_MINIMUM", response.reason()),
            () -> assertEquals(0, paymentRepository.count())
        );
    }

    @Test
    void should_generate_payment_when_beneficiary_is_eligible() {
        // REQ-033
        beneficiaryRepository.save(activeBeneficiary("11144477735", "P005"));
        socialProgramRepository.save(activeProgram("P005"));

        PaymentGenerationResponse response = paymentGenerationService.generate(
            new PaymentGenerationController.PaymentGenerationRequest("11144477735", 202609));

        assertAll(
            () -> assertEquals("GENERATED", response.outcome()),
            () -> assertEquals(1, paymentRepository.count())
        );
    }
}
