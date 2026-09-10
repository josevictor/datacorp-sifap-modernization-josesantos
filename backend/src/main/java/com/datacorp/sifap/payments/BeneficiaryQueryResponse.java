package com.datacorp.sifap.payments;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

/**
 * Cadastro do beneficiário e histórico recente de pagamentos (REQ-034 a
 * REQ-041).
 *
 * <p>O CPF trafega somente mascarado. O identificador estável do beneficiário
 * é {@code id}, para que a interface nunca precise do documento completo.
 */
public record BeneficiaryQueryResponse(
    UUID id,
    String maskedCpf,
    String fullName,
    String statusCode,
    String statusDescription,
    String programCode,
    BigDecimal familyIncome,
    int dependentCount,
    String regionCode,
    long nis,
    List<PaymentHistoryEntry> paymentHistory
) {

    /**
     * Item do histórico. O CPF não é repetido: ele já consta, mascarado, no
     * cabeçalho da resposta.
     */
    public record PaymentHistoryEntry(
        int referencePeriod,
        BigDecimal grossAmount,
        BigDecimal netAmount,
        String status,
        String paymentType
    ) {

        static PaymentHistoryEntry from(Payment payment) {
            return new PaymentHistoryEntry(
                payment.referencePeriod(),
                payment.grossAmount(),
                payment.netAmount(),
                payment.status(),
                payment.paymentType());
        }
    }

    static BeneficiaryQueryResponse of(Beneficiary beneficiary, List<Payment> payments) {
        return new BeneficiaryQueryResponse(
            beneficiary.id(),
            CpfMask.of(beneficiary.cpf()),
            beneficiary.fullName(),
            beneficiary.status(),
            BeneficiaryStatusDescription.of(beneficiary.status()),
            beneficiary.programCode(),
            beneficiary.familyIncome(),
            beneficiary.dependentCount(),
            beneficiary.regionCode(),
            beneficiary.nis(),
            payments.stream().map(PaymentHistoryEntry::from).toList());
    }

    /**
     * Indica ausência de pagamentos (REQ-041), para que a interface distinga
     * "sem pagamentos" de "lista ainda não carregada".
     */
    public boolean hasNoPayments() {
        return paymentHistory.isEmpty();
    }
}
