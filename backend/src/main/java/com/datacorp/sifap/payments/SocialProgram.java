package com.datacorp.sifap.payments;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.util.UUID;

@Entity
@Table(name = "social_program")
class SocialProgram {

    @Id
    private UUID id;

    @Column(nullable = false, length = 4, unique = true)
    private String code;

    @Column(nullable = false, length = 1)
    private String type;

    @Column(nullable = false, precision = 7, scale = 2)
    private BigDecimal baseIndividualAmount;

    @Column(nullable = false, precision = 5, scale = 4)
    private BigDecimal adjustmentFactor;

    @Column(nullable = false, length = 1)
    private String status;

    @Column(nullable = false, length = 5)
    private String eligibilityCode;

    @Column(nullable = false)
    private short ageMin;

    @Column(nullable = false)
    private short ageMax;

    @Column(nullable = false, precision = 7, scale = 2)
    private BigDecimal maxIncome;

    protected SocialProgram() {
    }

    SocialProgram(UUID id, String code, String type, BigDecimal baseIndividualAmount, BigDecimal adjustmentFactor, String status) {
        this(id, code, type, baseIndividualAmount, adjustmentFactor, status, "", (short) 0, (short) 0, BigDecimal.ZERO);
    }

    SocialProgram(
        UUID id,
        String code,
        String type,
        BigDecimal baseIndividualAmount,
        BigDecimal adjustmentFactor,
        String status,
        String eligibilityCode,
        short ageMin,
        short ageMax,
        BigDecimal maxIncome
    ) {
        this.id = id;
        this.code = code;
        this.type = type;
        this.baseIndividualAmount = baseIndividualAmount;
        this.adjustmentFactor = adjustmentFactor;
        this.status = status;
        this.eligibilityCode = eligibilityCode;
        this.ageMin = ageMin;
        this.ageMax = ageMax;
        this.maxIncome = maxIncome;
    }

    String code() {
        return code;
    }

    String type() {
        return type;
    }

    BigDecimal baseIndividualAmount() {
        return baseIndividualAmount;
    }

    BigDecimal adjustmentFactor() {
        return adjustmentFactor;
    }

    boolean isActive() {
        return "A".equals(status);
    }

    String eligibilityCode() {
        return eligibilityCode;
    }

    short ageMin() {
        return ageMin;
    }

    short ageMax() {
        return ageMax;
    }

    BigDecimal maxIncome() {
        return maxIncome;
    }
}
