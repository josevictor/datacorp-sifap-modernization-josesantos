package com.datacorp.sifap.payments;

record YearMonthPeriod(int value) {

    static YearMonthPeriod of(int value) {
        int month = value - ((value / 100) * 100);
        if (month < 1 || month > 12) {
            throw new PaymentGenerationRejectedException("Invalid period");
        }
        return new YearMonthPeriod(value);
    }

    int year() {
        return value / 100;
    }

    int month() {
        return value - (year() * 100);
    }
}
