package com.datacorp.sifap.payments;

public class PaymentGenerationNotFoundException extends RuntimeException {

    public PaymentGenerationNotFoundException(String message) {
        super(message);
    }
}
