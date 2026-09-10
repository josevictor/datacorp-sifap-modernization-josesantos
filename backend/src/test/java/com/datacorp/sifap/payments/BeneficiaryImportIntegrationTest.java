package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.datacorp.sifap.migration.LegacySeedData;
import java.io.IOException;
import java.io.InputStream;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Transactional
class BeneficiaryImportIntegrationTest {

    private static final String KNOWN_CPF = "78933359478";

    @Autowired
    private BeneficiaryImportService beneficiaryImportService;

    @Autowired
    private BeneficiaryRepository beneficiaryRepository;

    @Autowired
    private BeneficiaryQueryService beneficiaryQueryService;

    @Test
    void should_load_the_legacy_extract_and_account_for_every_record() throws IOException {
        ImportReport<BeneficiaryImportRejection> report = runImport();

        assertAll(
            () -> assertEquals(500, report.read()),
            () -> assertTrue(report.isReconciled(),
                () -> "carga não reconciliada: " + report),
            () -> assertTrue(report.loaded() > 0));
    }

    @Test
    void should_make_a_migrated_beneficiary_reachable_through_the_public_query() throws IOException {
        runImport();

        BeneficiaryQueryResponse response = beneficiaryQueryService.findByCpf(KNOWN_CPF);

        assertAll(
            () -> assertEquals("***.***.594-78", response.maskedCpf()),
            () -> assertEquals("MARIA MARTINS OLIVEIRA", response.fullName()),
            () -> assertEquals("A", response.statusCode()),
            () -> assertEquals(28566181479L, response.nis()));
    }

    @Test
    void should_preserve_the_packed_decimal_income_exactly() throws IOException {
        runImport();

        Optional<Beneficiary> migrated = beneficiaryRepository.findByCpf(KNOWN_CPF);

        assertTrue(migrated.isPresent());
        assertAll(
            () -> assertEquals(0, new BigDecimal("1000.00").compareTo(migrated.get().familyIncome())),
            () -> assertEquals("02", migrated.get().regionCode()),
            () -> assertEquals("PBF1", migrated.get().programCode()),
            () -> assertEquals(0, migrated.get().dependentCount()),
            () -> assertEquals(1946, migrated.get().birthYear()));
    }

    @Test
    void should_skip_already_loaded_records_when_the_import_runs_twice() throws IOException {
        ImportReport<BeneficiaryImportRejection> first = runImport();

        ImportReport<BeneficiaryImportRejection> second = runImport();

        // Reexecutar não pode transformar o NIS já gravado por um registro em
        // colisão contra ele mesmo: isso recusaria a extração inteira.
        assertAll(
            () -> assertEquals(0, second.loaded(), "a segunda execução não pode duplicar registros"),
            () -> assertEquals(first.loaded(), second.skipped()),
            () -> assertEquals(first.rejected().size(), second.rejected().size()),
            () -> assertFalse(
                second.rejected().stream()
                    .anyMatch(r -> r.reason() == BeneficiaryImportRejection.DUPLICATE_NIS),
                "um registro não colide com o próprio NIS já carregado"),
            () -> assertTrue(second.isReconciled()));
    }

    @Test
    void should_reject_records_only_for_documented_reasons() throws IOException {
        ImportReport<BeneficiaryImportRejection> report = runImport();

        Map<BeneficiaryImportRejection, Long> byReason = report.rejected().stream()
            .collect(Collectors.groupingBy(
                ImportReport.RejectedRecord::reason, Collectors.counting()));

        // Nenhum registro pode ser recusado por leiaute mal posicionado; esses
        // motivos denunciariam deslocamento, e não dado legado ruim.
        assertAll(
            () -> assertFalse(byReason.containsKey(BeneficiaryImportRejection.INVALID_STATUS),
                () -> "situação fora do domínio sugere deslocamento de campo: " + byReason),
            () -> assertFalse(byReason.containsKey(BeneficiaryImportRejection.UNKNOWN_REGION),
                () -> "região fora do domínio sugere deslocamento de campo: " + byReason),
            () -> assertFalse(byReason.containsKey(BeneficiaryImportRejection.INVALID_DOCS_FLAG),
                () -> "indicador de documentação inválido sugere deslocamento: " + byReason),
            () -> assertFalse(byReason.containsKey(BeneficiaryImportRejection.INVALID_BIRTH_DATE),
                () -> "data de nascimento inválida sugere deslocamento: " + byReason));
    }

    private ImportReport<BeneficiaryImportRejection> runImport() throws IOException {
        try (InputStream layout = Files.newInputStream(LegacySeedData.file("layout-beneficiary.txt"));
             InputStream data = Files.newInputStream(LegacySeedData.file("beneficiary.dat"))) {
            ImportReport<BeneficiaryImportRejection> report =
                beneficiaryImportService.importFrom(layout, data);
            assertNotNull(report);
            return report;
        }
    }
}
