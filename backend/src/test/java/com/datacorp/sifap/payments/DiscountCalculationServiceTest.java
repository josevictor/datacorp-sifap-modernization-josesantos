package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class DiscountCalculationServiceTest {

    private static final int TODAY = 20260910;

    private final DiscountCalculationService service = new DiscountCalculationService();

    @ParameterizedTest
    @CsvSource({
        "500.00, 15.00",
        "500.01, 25.00",
        "1000.00, 50.00",
        "1500.00, 105.00",
        "2000.00, 140.00",
        "5000.00, 450.00",
        "9999.99, 899.99"
    })
    void should_apply_social_contribution_band_matching_gross_amount(String gross, String expected) {
        // REQ-010
        Money total = service.totalFor(money(gross), List.of(), TODAY);

        assertEquals(new BigDecimal(expected), total.value());
    }

    @Test
    void should_apply_no_social_contribution_when_gross_exceeds_last_band() {
        // REQ-010
        Money total = service.totalFor(money("10000.00"), List.of(), TODAY);

        assertEquals(new BigDecimal("0.00"), total.value());
    }

    @Test
    void should_ignore_discount_when_end_date_is_in_the_past() {
        // REQ-012
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "P", "100.00", "0", 20200101, 20250101)),
            TODAY);

        assertEquals(new BigDecimal("50.00"), total.value());
    }

    @Test
    void should_consider_discount_effective_when_end_date_is_zero() {
        // REQ-012
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "P", "100.00", "0", 20200101, 0)),
            TODAY);

        assertEquals(new BigDecimal("150.00"), total.value());
    }

    @Test
    void should_ignore_discount_when_start_date_is_in_the_future() {
        // REQ-012
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "P", "100.00", "0", 20990101, 0)),
            TODAY);

        assertEquals(new BigDecimal("50.00"), total.value());
    }

    @Test
    void should_use_fixed_amount_when_court_ordered_discount_has_positive_amount() {
        // REQ-013
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "J", "200.00", "0", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("250.00"), total.value());
    }

    @Test
    void should_use_percentage_when_court_ordered_discount_has_no_fixed_amount() {
        // REQ-013
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "J", "0", "10.00", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("150.00"), total.value());
    }

    @Test
    void should_not_cap_total_when_only_court_ordered_discount_exceeds_cap() {
        // REQ-013
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "J", "800.00", "0", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("850.00"), total.value());
    }

    @Test
    void should_use_fixed_amount_for_alimony_discount() {
        // REQ-014
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "P", "80.00", "0", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("130.00"), total.value());
    }

    @Test
    void should_use_percentage_for_administrative_discount_without_fixed_amount() {
        // REQ-014
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "A", "0", "5.00", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("100.00"), total.value());
    }

    @Test
    void should_ignore_fixed_amount_for_withholding_tax_discount() {
        // REQ-015
        Money withFixedAmount = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "I", "999.00", "10.00", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("150.00"), withFixedAmount.value());
    }

    @Test
    void should_apply_registered_percentage_for_withholding_tax_discount() {
        // REQ-015
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "I", "0", "7.50", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("125.00"), total.value());
    }

    @Test
    void should_apply_fixed_one_percent_rate_for_union_dues_discount() {
        // REQ-016
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "S", "500.00", "9.00", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("60.00"), total.value());
    }

    @Test
    void should_ignore_discount_when_type_is_unknown() {
        // REQ-017
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "X", "500.00", "50.00", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("50.00"), total.value());
    }

    @Test
    void should_keep_processing_valid_discount_after_unknown_type() {
        // REQ-017
        Money total = service.totalFor(
            money("1000.00"),
            List.of(
                discount(1, "X", "500.00", "0", 0, 0),
                discount(2, "P", "100.00", "0", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("150.00"), total.value());
    }

    @Test
    void should_cap_total_when_non_court_ordered_discount_exceeds_cap() {
        // REQ-011, REQ-018
        Money total = service.totalFor(
            money("1000.00"),
            List.of(discount(1, "I", "0", "40.00", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("300.00"), total.value());
    }

    @Test
    void should_cap_accumulated_total_after_union_dues_follows_court_ordered_discount() {
        // REQ-018
        // Comportamento legado preservado deliberadamente: o desconto judicial
        // é declarado isento de teto, mas um item posterior não judicial
        // limita o total acumulado e reduz o valor originado dele.
        // Achado BONUS em 01-archaeology/mysteries-found.md.
        Money total = service.totalFor(
            money("1000.00"),
            List.of(
                discount(1, "J", "800.00", "0", 0, 0),
                discount(2, "S", "0", "0", 0, 0)),
            TODAY);

        assertEquals(new BigDecimal("300.00"), total.value());
    }

    @Test
    void should_depend_on_discount_order_when_cap_is_reached() {
        // REQ-018
        // Documenta que a ordem de cadastro altera o líquido pago.
        Money unionDuesFirst = service.totalFor(
            money("1000.00"),
            List.of(
                discount(1, "S", "0", "0", 0, 0),
                discount(2, "J", "800.00", "0", 0, 0)),
            TODAY);

        Money courtOrderedFirst = service.totalFor(
            money("1000.00"),
            List.of(
                discount(1, "J", "800.00", "0", 0, 0),
                discount(2, "S", "0", "0", 0, 0)),
            TODAY);

        assertAll(
            () -> assertEquals(new BigDecimal("860.00"), unionDuesFirst.value()),
            () -> assertEquals(new BigDecimal("300.00"), courtOrderedFirst.value())
        );
    }

    private Money money(String value) {
        return new Money(new BigDecimal(value));
    }

    private PaymentDiscount discount(
        int sequence, String type, String fixedAmount, String percentage, int startDate, int endDate) {
        return new PaymentDiscount(
            UUID.randomUUID(),
            UUID.randomUUID(),
            sequence,
            type,
            new BigDecimal(fixedAmount),
            new BigDecimal(percentage),
            startDate,
            endDate,
            null);
    }
}
