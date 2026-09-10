package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigDecimal;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class PaymentCalculationServiceTest {

    private final PaymentCalculationService service = new PaymentCalculationService();

    @Test
    void should_calculate_gross_amount_when_factors_are_known() {
        // REQ-005
        PaymentCalculation calculation = service.calculate(
            beneficiary("01", 19800101, 2, "01", "400.00"),
            program("P", "100.00", "0.1000"),
            YearMonthPeriod.of(202609));

        assertEquals(new BigDecimal("138.84"), calculation.grossAmount().value());
    }

    @Test
    void should_calculate_december_type_and_bonus_when_program_type_is_a() {
        // REQ-006, REQ-007
        PaymentCalculation calculation = service.calculate(
            beneficiary("15", 19800101, 0, "15", "100.00"),
            program("A", "100.00", "0.0000"),
            YearMonthPeriod.of(202612));

        assertAll(
            () -> assertEquals("D", calculation.paymentType()),
            () -> assertEquals(new BigDecimal("15.00"), calculation.bonusAmount().value()),
            () -> assertEquals(new BigDecimal("215.00"), calculation.grossAmount().value())
        );
    }

    @Test
    void should_calculate_normal_type_and_zero_bonus_when_period_is_not_december() {
        // REQ-006, REQ-007
        PaymentCalculation calculation = service.calculate(
            beneficiary("01", 19800101, 0, "15", "100.00"),
            program("A", "100.00", "0.0000"),
            YearMonthPeriod.of(202611));

        assertAll(
            () -> assertEquals("N", calculation.paymentType()),
            () -> assertEquals(new BigDecimal("0.00"), calculation.bonusAmount().value())
        );
    }

    @Test
    void should_truncate_amounts_when_fraction_has_more_than_two_decimal_places() {
        // REQ-005
        PaymentCalculation calculation = service.calculate(
            beneficiary("01", 19800101, 0, "01", "100.00"),
            program("P", "100.01", "0.0000"),
            YearMonthPeriod.of(202609));

        assertEquals(new BigDecimal("135.01"), calculation.grossAmount().value());
    }

    @Test
    void should_return_zero_net_amount_when_discount_exceeds_gross() {
        // REQ-008
        Money net = service.netAmount(new Money(new BigDecimal("10.00")), new Money(new BigDecimal("11.00")));

        assertEquals(new BigDecimal("0.00"), net.value());
    }

    @Test
    void should_keep_positive_net_amount_when_discount_is_lower_than_gross() {
        // REQ-008
        Money net = service.netAmount(new Money(new BigDecimal("10.00")), new Money(new BigDecimal("1.25")));

        assertEquals(new BigDecimal("8.75"), net.value());
    }

    private Beneficiary beneficiary(String regionCode, int birthDate, int dependents, String programCode, String income) {
        return new Beneficiary(
            UUID.randomUUID(),
            "52998224725",
            "Pessoa Beneficiaria",
            birthDate,
            "A",
            programCode,
            new BigDecimal(income),
            dependents,
            regionCode);
    }

    private SocialProgram program(String type, String baseAmount, String adjustmentFactor) {
        return new SocialProgram(UUID.randomUUID(), "P001", type, new BigDecimal(baseAmount), new BigDecimal(adjustmentFactor), "A");
    }
}
