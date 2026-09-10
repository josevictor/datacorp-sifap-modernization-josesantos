package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.datacorp.sifap.migration.LegacySeedData;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Transactional
class PaymentImportIntegrationTest {

    private static final String KNOWN_CPF = "78933359478";

    @Autowired
    private BeneficiaryImportService beneficiaryImportService;

    @Autowired
    private PaymentImportService paymentImportService;

    @Autowired
    private BeneficiaryQueryService beneficiaryQueryService;

    @Test
    void should_load_the_payment_extract_and_account_for_every_record() throws IOException {
        importBeneficiaries();

        ImportReport<PaymentImportRejection> report = importPayments();

        assertAll(
            () -> assertEquals(2000, report.read()),
            () -> assertTrue(report.isReconciled()),
            () -> assertTrue(report.loaded() > 0));
    }

    @Test
    void should_expose_the_migrated_history_through_the_beneficiary_query() throws IOException {
        importBeneficiaries();
        importPayments();

        BeneficiaryQueryResponse response = beneficiaryQueryService.findByCpf(KNOWN_CPF);

        assertAll(
            () -> assertEquals("MARIA MARTINS OLIVEIRA", response.fullName()),
            () -> assertFalse(response.paymentHistory().isEmpty(), "o histórico migrado deve aparecer"),
            () -> assertEquals(4, response.paymentHistory().size()));
    }

    @Test
    void should_return_the_migrated_history_from_the_newest_period_to_the_oldest() throws IOException {
        // REQ-040 — a ordenação explícita corrige o LAST 12 do legado, que lê
        // pelo descritor de CPF e corta na décima segunda ocorrência.
        importBeneficiaries();
        importPayments();

        List<Integer> periods = beneficiaryQueryService.findByCpf(KNOWN_CPF).paymentHistory().stream()
            .map(BeneficiaryQueryResponse.PaymentHistoryEntry::referencePeriod)
            .toList();

        assertEquals(
            periods.stream().sorted(Comparator.reverseOrder()).toList(),
            periods);
    }

    @Test
    void should_preserve_legacy_amounts_without_recalculating_them() throws IOException {
        importBeneficiaries();
        importPayments();

        BeneficiaryQueryResponse.PaymentHistoryEntry latest =
            beneficiaryQueryService.findByCpf(KNOWN_CPF).paymentHistory().get(0);

        // Os valores vêm da origem: recalcular usaria fatores regionais atuais,
        // que divergem dos vigentes quando o pagamento foi apurado.
        assertAll(
            () -> assertTrue(latest.grossAmount().signum() > 0),
            () -> assertTrue(latest.netAmount().signum() >= 0),
            () -> assertEquals(2, latest.grossAmount().scale()),
            () -> assertEquals(2, latest.netAmount().scale()));
    }

    @Test
    void should_skip_already_loaded_payments_when_the_import_runs_twice() throws IOException {
        importBeneficiaries();
        ImportReport<PaymentImportRejection> first = importPayments();

        ImportReport<PaymentImportRejection> second = importPayments();

        assertAll(
            () -> assertEquals(0, second.loaded(), "a segunda execução não pode duplicar pagamentos"),
            () -> assertEquals(first.loaded(), second.skipped()),
            () -> assertTrue(second.isReconciled()));
    }

    @Test
    void should_reject_every_payment_when_no_beneficiary_was_loaded() throws IOException {
        // Sem o cadastro carregado, o pagamento não é exibível pela consulta;
        // recusar é preferível a gravar um histórico órfão.
        ImportReport<PaymentImportRejection> report = importPayments();

        Map<PaymentImportRejection, Long> byReason = report.rejected().stream()
            .collect(Collectors.groupingBy(
                ImportReport.RejectedRecord::reason, Collectors.counting()));

        assertAll(
            () -> assertEquals(0, report.loaded()),
            () -> assertEquals(2000L, byReason.get(PaymentImportRejection.UNKNOWN_BENEFICIARY)),
            () -> assertTrue(report.isReconciled()));
    }

    @Test
    void should_not_reject_payments_for_reasons_that_would_signal_a_shifted_layout() throws IOException {
        importBeneficiaries();

        ImportReport<PaymentImportRejection> report = importPayments();

        Map<PaymentImportRejection, Long> byReason = report.rejected().stream()
            .collect(Collectors.groupingBy(
                ImportReport.RejectedRecord::reason, Collectors.counting()));

        assertAll(
            () -> assertFalse(byReason.containsKey(PaymentImportRejection.INVALID_STATUS),
                () -> "situação fora do domínio sugere deslocamento de campo: " + byReason),
            () -> assertFalse(byReason.containsKey(PaymentImportRejection.INVALID_PAYMENT_TYPE),
                () -> "tipo de pagamento inválido sugere deslocamento: " + byReason),
            () -> assertFalse(byReason.containsKey(PaymentImportRejection.INVALID_PERIOD),
                () -> "período inválido sugere deslocamento: " + byReason),
            () -> assertFalse(byReason.containsKey(PaymentImportRejection.INVALID_GENERATION_DATE),
                () -> "data de geração inválida sugere deslocamento: " + byReason));
    }

    private void importBeneficiaries() throws IOException {
        try (InputStream layout = Files.newInputStream(LegacySeedData.file("layout-beneficiary.txt"));
             InputStream data = Files.newInputStream(LegacySeedData.file("beneficiary.dat"))) {
            assertNotNull(beneficiaryImportService.importFrom(layout, data));
        }
    }

    private ImportReport<PaymentImportRejection> importPayments() throws IOException {
        try (InputStream layout = Files.newInputStream(LegacySeedData.file("layout-payment.txt"));
             InputStream data = Files.newInputStream(LegacySeedData.file("payment.dat"))) {
            return paymentImportService.importFrom(layout, data);
        }
    }
}
