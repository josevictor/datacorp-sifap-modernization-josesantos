package com.datacorp.sifap.payments;

import java.math.BigDecimal;
import java.math.RoundingMode;

record Money(BigDecimal value) {

    Money {
        if (value == null) {
            throw new IllegalArgumentException("Amount is required");
        }
        value = truncate(value);
    }

    static Money zero() {
        return new Money(BigDecimal.ZERO);
    }

    Money add(Money other) {
        return new Money(value.add(other.value));
    }

    Money subtract(Money other) {
        return new Money(value.subtract(other.value));
    }

    Money multiply(BigDecimal factor) {
        return new Money(value.multiply(factor));
    }

    boolean isNegative() {
        return value.signum() < 0;
    }

    boolean isGreaterThan(Money other) {
        return value.compareTo(other.value) > 0;
    }

    private static BigDecimal truncate(BigDecimal amount) {
        return amount.setScale(2, RoundingMode.DOWN);
    }
}
