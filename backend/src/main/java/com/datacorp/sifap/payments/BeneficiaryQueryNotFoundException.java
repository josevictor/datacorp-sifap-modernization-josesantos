package com.datacorp.sifap.payments;

public class BeneficiaryQueryNotFoundException extends RuntimeException {

    public BeneficiaryQueryNotFoundException(String message) {
        super(message);
    }
}
