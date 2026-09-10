package com.datacorp.sifap.payments;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.util.UUID;

@Entity
@Table(name = "beneficiary")
class Beneficiary {

    @Id
    private UUID id;

    @Column(nullable = false, length = 11, unique = true)
    private String cpf;

    @Column(nullable = false, length = 60)
    private String fullName;

    @Column(nullable = false)
    private int birthDate;

    @Column(nullable = false, length = 1)
    private String status;

    @Column(nullable = false, length = 4)
    private String programCode;

    @Column(nullable = false, precision = 9, scale = 2)
    private BigDecimal familyIncome;

    @Column(nullable = false)
    private int dependentCount;

    @Column(nullable = false, length = 2)
    private String regionCode;

    @Column(nullable = false)
    private long nis;

    @Column(nullable = false, length = 1)
    private String docsOk;

    protected Beneficiary() {
    }

    Beneficiary(
        UUID id,
        String cpf,
        String fullName,
        int birthDate,
        String status,
        String programCode,
        BigDecimal familyIncome,
        int dependentCount,
        String regionCode
    ) {
        this(id, cpf, fullName, birthDate, status, programCode, familyIncome, dependentCount, regionCode, 0L, "S");
    }

    Beneficiary(
        UUID id,
        String cpf,
        String fullName,
        int birthDate,
        String status,
        String programCode,
        BigDecimal familyIncome,
        int dependentCount,
        String regionCode,
        long nis,
        String docsOk
    ) {
        this.id = id;
        this.cpf = cpf;
        this.fullName = fullName;
        this.birthDate = birthDate;
        this.status = status;
        this.programCode = programCode;
        this.familyIncome = familyIncome;
        this.dependentCount = dependentCount;
        this.regionCode = regionCode;
        this.nis = nis;
        this.docsOk = docsOk;
    }

    String cpf() {
        return cpf;
    }

    UUID id() {
        return id;
    }

    String fullName() {
        return fullName;
    }

    int birthYear() {
        return birthDate / 10000;
    }

    boolean isActive() {
        return "A".equals(status);
    }

    String programCode() {
        return programCode;
    }

    BigDecimal familyIncome() {
        return familyIncome;
    }

    int dependentCount() {
        return dependentCount;
    }

    String regionCode() {
        return regionCode;
    }

    String status() {
        return status;
    }

    long nis() {
        return nis;
    }

    boolean hasCompleteDocumentation() {
        return "S".equals(docsOk);
    }
}
