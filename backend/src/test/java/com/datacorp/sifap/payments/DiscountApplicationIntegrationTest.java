package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;

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
class DiscountApplicationIntegrationTest {

    @Autowired
    private BeneficiaryRepository beneficiaryRepository;

    @Autowired
    private SocialProgramRepository socialProgramRepository;

    @Autowired
    private PaymentRepository paymentRepository;

    @Autowired
    private PaymentDiscountRepository paymentDiscountRepository;

    @Autowired
    private PaymentGenerationService paymentGenerationService;

    @Autowired
    private DiscountApplicationService discountApplicationService;

    @Test
    void should_persist_truncated_discount_total_and_recalculate_net_amount() {
        // REQ-019
        UUID paymentId = generatePayment("52998224725", "P001");
        // Bruto 1000,00: contribuição social de 5% mais alimentos de 80,00.
        paymentDiscountRepository.save(discount(paymentId, 1, "P", "80.00", "0"));

        DiscountApplicationResponse response = discountApplicationService.apply(paymentId);

        assertAll(
            () -> assertEquals(new BigDecimal("1000.00"), response.grossAmount()),
            () -> assertEquals(new BigDecimal("130.00"), response.discountAmount()),
            () -> assertEquals(new BigDecimal("870.00"), response.netAmount()),
            () -> assertEquals(1, response.appliedDiscountCount())
        );
    }

    @Test
    void should_apply_only_social_contribution_when_payment_has_no_registered_discount() {
        // REQ-010, REQ-019
        UUID paymentId = generatePayment("11144477735", "P002");

        DiscountApplicationResponse response = discountApplicationService.apply(paymentId);

        assertAll(
            () -> assertEquals(new BigDecimal("50.00"), response.discountAmount()),
            () -> assertEquals(new BigDecimal("950.00"), response.netAmount()),
            () -> assertEquals(0, response.appliedDiscountCount())
        );
    }

    @Test
    void should_cap_persisted_total_at_thirty_percent_of_gross_amount() {
        // REQ-011, REQ-018, REQ-019
        UUID paymentId = generatePayment("52998224725", "P001");
        paymentDiscountRepository.save(discount(paymentId, 1, "I", "0", "40.00"));

        DiscountApplicationResponse response = discountApplicationService.apply(paymentId);

        assertAll(
            () -> assertEquals(new BigDecimal("300.00"), response.discountAmount()),
            () -> assertEquals(new BigDecimal("700.00"), response.netAmount())
        );
    }

    @Test
    void should_reflect_persisted_total_when_payment_is_read_again() {
        // REQ-019
        UUID paymentId = generatePayment("52998224725", "P001");
        paymentDiscountRepository.save(discount(paymentId, 1, "S", "0", "0"));

        discountApplicationService.apply(paymentId);
        Payment stored = paymentRepository.findById(paymentId).orElseThrow();

        assertAll(
            () -> assertEquals(new BigDecimal("60.00"), stored.discountAmount()),
            () -> assertEquals(new BigDecimal("940.00"), stored.netAmount())
        );
    }

    /** Gera um pagamento com bruto de 1000,00 para simplificar as conferências. */
    private UUID generatePayment(String cpf, String programCode) {
        beneficiaryRepository.save(new Beneficiary(
            UUID.randomUUID(), cpf, "Pessoa Beneficiaria", 19800101, "A", programCode,
            new BigDecimal("100.00"), 0, "15"));
        // Tipo 'A': o beneficiário do fixture tem 46 anos no período e o tipo
        // 'P' exigiria 60 anos (REQ-028), tornando a geração inelegível. O
        // bruto permanece 1000,00, porque o abono do tipo 'A' só incide em
        // dezembro.
        socialProgramRepository.save(new SocialProgram(
            UUID.randomUUID(), programCode, "A", new BigDecimal("1000.00"), BigDecimal.ZERO, "A"));

        PaymentGenerationResponse generated = paymentGenerationService.generate(
            new PaymentGenerationController.PaymentGenerationRequest(cpf, 202609));

        return generated.paymentId();
    }

    private PaymentDiscount discount(
        UUID paymentId, int sequence, String type, String fixedAmount, String percentage) {
        return new PaymentDiscount(
            UUID.randomUUID(),
            paymentId,
            sequence,
            type,
            new BigDecimal(fixedAmount),
            new BigDecimal(percentage),
            0,
            0,
            null);
    }
}
