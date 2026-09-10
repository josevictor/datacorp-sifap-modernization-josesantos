package com.datacorp.sifap.payments;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "payment_rejection")
class PaymentRejection {

    @Id
    private UUID id;

    @Column(nullable = false, length = 11)
    private String cpf;

    @Column(nullable = false)
    private int referencePeriod;

    @Column(nullable = false, length = 40)
    private String reason;

    @Column(nullable = false)
    private OffsetDateTime createdAt;

    protected PaymentRejection() {
    }

    private PaymentRejection(UUID id, String cpf, int referencePeriod, String reason, OffsetDateTime createdAt) {
        this.id = id;
        this.cpf = cpf;
        this.referencePeriod = referencePeriod;
        this.reason = reason;
        this.createdAt = createdAt;
    }

    static PaymentRejection of(String cpf, YearMonthPeriod period, String reason, OffsetDateTime createdAt) {
        return new PaymentRejection(UUID.randomUUID(), cpf, period.value(), reason, createdAt);
    }
}
