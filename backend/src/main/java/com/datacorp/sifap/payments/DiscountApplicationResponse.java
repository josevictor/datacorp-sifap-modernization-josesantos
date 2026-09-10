package com.datacorp.sifap.payments;

import java.math.BigDecimal;
import java.util.UUID;

public record DiscountApplicationResponse(
    UUID paymentId,
    int period,
    BigDecimal grossAmount,
    BigDecimal discountAmount,
    BigDecimal netAmount,
    int appliedDiscountCount
) {

    static DiscountApplicationResponse of(Payment payment, int appliedDiscountCount) {
        return new DiscountApplicationResponse(
            payment.id(),
            payment.referencePeriod(),
            payment.grossAmount(),
            payment.discountAmount(),
            payment.netAmount(),
            appliedDiscountCount);
    }
}
