package com.datacorp.sifap.payments;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.util.UUID;

/**
 * Desconto registrado para um pagamento.
 *
 * <p>Equivale a uma ocorrência do grupo periódico {@code GRP-DISC} do DDM
 * {@code PAYMENT}. As datas usam o formato numérico {@code YYYYMMDD} do
 * legado porque {@code endDate == 0} significa "sem término" (REQ-012).
 */
@Entity
@Table(name = "payment_discount")
class PaymentDiscount {

    @Id
    private UUID id;

    @Column(name = "payment_id", nullable = false)
    private UUID paymentId;

    @Column(name = "sequence_number", nullable = false)
    private int sequenceNumber;

    @Column(nullable = false, length = 1)
    private String type;

    @Column(name = "fixed_amount", nullable = false)
    private BigDecimal fixedAmount;

    @Column(nullable = false)
    private BigDecimal percentage;

    @Column(name = "start_date", nullable = false)
    private int startDate;

    @Column(name = "end_date", nullable = false)
    private int endDate;

    @Column(name = "case_number", length = 20)
    private String caseNumber;

    protected PaymentDiscount() {
    }

    PaymentDiscount(
        UUID id,
        UUID paymentId,
        int sequenceNumber,
        String type,
        BigDecimal fixedAmount,
        BigDecimal percentage,
        int startDate,
        int endDate,
        String caseNumber
    ) {
        this.id = id;
        this.paymentId = paymentId;
        this.sequenceNumber = sequenceNumber;
        this.type = type;
        this.fixedAmount = fixedAmount;
        this.percentage = percentage;
        this.startDate = startDate;
        this.endDate = endDate;
        this.caseNumber = caseNumber;
    }

    String type() {
        return type;
    }

    BigDecimal fixedAmount() {
        return fixedAmount;
    }

    BigDecimal percentage() {
        return percentage;
    }

    /**
     * Indica se o desconto está vigente na data informada (REQ-012).
     *
     * <p>Data final igual a zero representa desconto sem término.
     */
    boolean isEffectiveOn(int referenceDate) {
        if (endDate != 0 && endDate < referenceDate) {
            return false;
        }
        return startDate <= referenceDate;
    }
}
