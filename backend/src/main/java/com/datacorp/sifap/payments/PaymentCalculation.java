package com.datacorp.sifap.payments;

record PaymentCalculation(
    Money grossAmount,
    Money discountAmount,
    Money bonusAmount,
    Money netAmount,
    String paymentType
) {
}
