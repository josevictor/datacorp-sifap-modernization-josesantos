package com.datacorp.sifap.migration;

import com.datacorp.sifap.payments.BeneficiaryImportService;
import com.datacorp.sifap.payments.ImportReport;
import com.datacorp.sifap.payments.PaymentImportService;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.Map;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

/**
 * Executa a carga da extração legada na inicialização, quando explicitamente
 * habilitada por {@code sifap.legacy-import.enabled}.
 *
 * <p>A carga é uma operação, não uma migração de esquema: mantê-la fora do
 * Flyway evita que os registros de laboratório se tornem obrigatórios em todo
 * ambiente e em toda suíte de testes. Como as importações são idempotentes,
 * repetir a execução é seguro.
 *
 * <p>Beneficiários são carregados antes dos pagamentos, porque um pagamento
 * sem cadastro correspondente é recusado.
 *
 * <p>O relatório é registrado de forma agregada. Nenhum CPF ou nome aparece no
 * log; registros recusados são identificados pela linha e pelo identificador
 * de origem.
 */
@Component
@ConditionalOnProperty(name = "sifap.legacy-import.enabled", havingValue = "true")
class LegacyImportRunner implements ApplicationRunner {

    private static final Logger LOG = LoggerFactory.getLogger(LegacyImportRunner.class);
    private static final int SAMPLE_SIZE = 10;

    private final BeneficiaryImportService beneficiaryImportService;
    private final PaymentImportService paymentImportService;
    private final Path seedDirectory;

    LegacyImportRunner(
        BeneficiaryImportService beneficiaryImportService,
        PaymentImportService paymentImportService,
        @Value("${sifap.legacy-import.directory}") Path seedDirectory
    ) {
        this.beneficiaryImportService = beneficiaryImportService;
        this.paymentImportService = paymentImportService;
        this.seedDirectory = seedDirectory;
    }

    @Override
    public void run(ApplicationArguments args) throws Exception {
        LOG.info("Carga legada iniciada a partir de {}", seedDirectory.toAbsolutePath());

        importBeneficiaries();
        importPayments();

        LOG.info("Carga legada finalizada");
    }

    private void importBeneficiaries() throws Exception {
        Path layoutFile = require("layout-beneficiary.txt");
        Path dataFile = require("beneficiary.dat");

        ImportReport<?> report;
        try (InputStream layout = Files.newInputStream(layoutFile);
             InputStream data = Files.newInputStream(dataFile)) {
            report = beneficiaryImportService.importFrom(layout, data);
        }
        report("Beneficiarios", report);
    }

    private void importPayments() throws Exception {
        Path layoutFile = require("layout-payment.txt");
        Path dataFile = require("payment.dat");

        ImportReport<?> report;
        try (InputStream layout = Files.newInputStream(layoutFile);
             InputStream data = Files.newInputStream(dataFile)) {
            report = paymentImportService.importFrom(layout, data);
        }
        report("Pagamentos", report);
    }

    private Path require(String fileName) {
        Path file = seedDirectory.resolve(fileName);
        if (!Files.isReadable(file)) {
            throw new IllegalStateException(
                "Arquivo da extração legada ausente ou ilegível: %s".formatted(file.toAbsolutePath()));
        }
        return file;
    }

    private void report(String label, ImportReport<?> report) {
        LOG.info(
            "{}: lidos={} carregados={} ignorados={} recusados={}",
            label, report.read(), report.loaded(), report.skipped(), report.rejected().size());

        if (!report.rejected().isEmpty()) {
            logRejections(label, report);
        }
        // A identidade lidos = carregados + ignorados + recusados é o que separa
        // uma carga completa de uma que perdeu registros pelo caminho.
        if (!report.isReconciled()) {
            throw new IllegalStateException(
                "%s: carga não reconciliada — lidos=%d carregados=%d ignorados=%d recusados=%d"
                    .formatted(label, report.read(), report.loaded(),
                        report.skipped(), report.rejected().size()));
        }
    }

    private void logRejections(String label, ImportReport<?> report) {
        Map<String, Long> byReason = report.rejected().stream()
            .collect(Collectors.groupingBy(
                rejected -> rejected.reason().name(), Collectors.counting()));

        byReason.entrySet().stream()
            .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
            .forEach(entry -> LOG.warn("{} recusados por {}: {}", label, entry.getKey(), entry.getValue()));

        report.rejected().stream()
            .sorted(Comparator.comparingLong(ImportReport.RejectedRecord::lineNumber))
            .limit(SAMPLE_SIZE)
            .forEach(rejected -> LOG.warn(
                "{} recusado: linha={} referencia={} motivo={}",
                label, rejected.lineNumber(), rejected.reference(), rejected.reason()));
    }
}
