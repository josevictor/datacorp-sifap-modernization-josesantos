package com.datacorp.sifap.payments;

public class PaymentGenerationRejectedException extends RuntimeException {

    public PaymentGenerationRejectedException(String message) {
        super(message);
    }
}
