package com.datacorp.sifap.payments;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name = "payment")
class Payment {

    @Id
    private UUID id;

    @Column(nullable = false, length = 11)
    private String cpf;

    @Column(nullable = false, length = 4)
    private String programCode;

    @Column(nullable = false)
    private int referencePeriod;

    @Column(nullable = false, precision = 9, scale = 2)
    private BigDecimal grossAmount;

    @Column(nullable = false, precision = 7, scale = 2)
    private BigDecimal discountAmount;

    @Column(nullable = false, precision = 9, scale = 2)
    private BigDecimal netAmount;

    @Column(nullable = false)
    private LocalDate generationDate;

    @Column(nullable = false, length = 1)
    private String status;

    @Column(nullable = false, length = 1)
    private String paymentType;

    @Column(nullable = false, precision = 9, scale = 2)
    private BigDecimal bonusAmount;

    protected Payment() {
    }

    private Payment(
        UUID id,
        String cpf,
        String programCode,
        int referencePeriod,
        PaymentCalculation calculation,
        LocalDate generationDate
    ) {
        this.id = id;
        this.cpf = cpf;
        this.programCode = programCode;
        this.referencePeriod = referencePeriod;
        this.grossAmount = calculation.grossAmount().value();
        this.discountAmount = calculation.discountAmount().value();
        this.netAmount = calculation.netAmount().value();
        this.generationDate = generationDate;
        this.status = "G";
        this.paymentType = calculation.paymentType();
        this.bonusAmount = calculation.bonusAmount().value();
    }

    static Payment generated(
        String cpf,
        String programCode,
        YearMonthPeriod period,
        PaymentCalculation calculation,
        LocalDate generationDate
    ) {
        return new Payment(UUID.randomUUID(), cpf, programCode, period.value(), calculation, generationDate);
    }

    /**
     * Reconstrói um pagamento já processado pelo sistema legado.
     *
     * <p>Os valores são preservados como foram apurados na origem, sem
     * recálculo. O fator regional aplicado pelo legado ao longo dos anos não é
     * reconstituível a partir do estado atual das tabelas, e recalcular
     * substituiria o histórico real por uma reconstrução que nunca ocorreu.
     *
     * <p>A situação também vem da origem, em vez do {@code "G"} atribuído a um
     * pagamento recém-gerado: o histórico contém pagamentos confirmados,
     * pagos, devolvidos e estornados.
     */
    static Payment migrated(
        String cpf,
        String programCode,
        int referencePeriod,
        BigDecimal grossAmount,
        BigDecimal discountAmount,
        BigDecimal netAmount,
        BigDecimal bonusAmount,
        LocalDate generationDate,
        String status,
        String paymentType
    ) {
        Payment payment = new Payment();
        payment.id = UUID.randomUUID();
        payment.cpf = cpf;
        payment.programCode = programCode;
        payment.referencePeriod = referencePeriod;
        payment.grossAmount = grossAmount;
        payment.discountAmount = discountAmount;
        payment.netAmount = netAmount;
        payment.bonusAmount = bonusAmount;
        payment.generationDate = generationDate;
        payment.status = status;
        payment.paymentType = paymentType;
        return payment;
    }

    UUID id() {
        return id;
    }

    String cpf() {
        return cpf;
    }

    String programCode() {
        return programCode;
    }

    int referencePeriod() {
        return referencePeriod;
    }

    BigDecimal grossAmount() {
        return grossAmount;
    }

    BigDecimal discountAmount() {
        return discountAmount;
    }

    BigDecimal netAmount() {
        return netAmount;
    }

    LocalDate generationDate() {
        return generationDate;
    }

    String status() {
        return status;
    }

    String paymentType() {
        return paymentType;
    }

    BigDecimal bonusAmount() {
        return bonusAmount;
    }

    /**
     * Aplica o total de descontos apurado e recalcula o líquido (REQ-019).
     *
     * <p>Equivale ao {@code UPDATE PAYMENT-V} executado por
     * {@code CALCDSCT.NSP} ao final do processamento. O líquido nunca é
     * negativo, conforme a regra preservada em {@code REQ-008}.
     */
    void applyDiscountTotal(Money discountTotal) {
        this.discountAmount = discountTotal.value();
        Money net = new Money(grossAmount).subtract(discountTotal);
        this.netAmount = net.isNegative() ? Money.zero().value() : net.value();
    }
}
