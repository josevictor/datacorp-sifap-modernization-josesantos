package com.datacorp.sifap.payments;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

public record PaymentGenerationResponse(
    String outcome,
    String reason,
    UUID paymentId,
    String cpf,
    String programCode,
    Integer period,
    BigDecimal grossAmount,
    BigDecimal discountAmount,
    BigDecimal netAmount,
    BigDecimal bonusAmount,
    String paymentType,
    String status,
    LocalDate generationDate
) {

    static PaymentGenerationResponse ignored(String reason) {
        return new PaymentGenerationResponse(
            "IGNORED", reason, null, null, null, null, null, null, null, null, null, null, null);
    }

    static PaymentGenerationResponse rejected(String reason) {
        return new PaymentGenerationResponse(
            "REJECTED", reason, null, null, null, null, null, null, null, null, null, null, null);
    }

    static PaymentGenerationResponse generated(Payment payment) {
        return new PaymentGenerationResponse(
            "GENERATED",
            null,
            payment.id(),
            payment.cpf(),
            payment.programCode(),
            payment.referencePeriod(),
            payment.grossAmount(),
            payment.discountAmount(),
            payment.netAmount(),
            payment.bonusAmount(),
            payment.paymentType(),
            payment.status(),
            payment.generationDate());
    }
}
