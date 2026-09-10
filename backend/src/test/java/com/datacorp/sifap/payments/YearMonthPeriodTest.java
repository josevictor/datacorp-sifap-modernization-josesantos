package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrowsExactly;

import org.junit.jupiter.api.Test;

class YearMonthPeriodTest {

    @Test
    void should_accept_period_when_month_is_valid() {
        // REQ-001
        YearMonthPeriod period = YearMonthPeriod.of(202609);

        assertAll(
            () -> assertEquals(2026, period.year()),
            () -> assertEquals(9, period.month())
        );
    }

    @Test
    void should_reject_period_when_month_is_invalid() {
        // REQ-001
        assertThrowsExactly(PaymentGenerationRejectedException.class, () -> YearMonthPeriod.of(202613));
    }
}
