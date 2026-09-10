package com.datacorp.sifap.payments;

import com.datacorp.sifap.migration.FixedWidthLayout;
import com.datacorp.sifap.migration.LegacyPaymentReader;
import com.datacorp.sifap.migration.LegacyPaymentRecord;
import java.io.IOException;
import java.io.InputStream;
import java.math.BigDecimal;
import java.time.DateTimeException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Carrega o histórico de pagamentos da extração legada.
 *
 * <p>Os valores são migrados como foram apurados na origem, sem recálculo.
 * Recalcular produziria números diferentes: os fatores regionais mudaram ao
 * longo dos anos e o estado atual das tabelas não reconstitui o que vigorava
 * em cada período. O histórico é registro do que aconteceu, não do que
 * aconteceria sob as regras de hoje.
 *
 * <p>A carga é idempotente pelo par CPF e período de referência, que é a chave
 * única da tabela {@code payment}, e exige o beneficiário já carregado: um
 * pagamento sem cadastro correspondente não é exibível pela consulta e
 * indicaria carga fora de ordem.
 */
@Service
public class PaymentImportService {

    private static final Set<String> VALID_STATUSES = Set.of("C", "P", "G", "D", "E", "R", "X");
    private static final Set<String> VALID_PAYMENT_TYPES = Set.of("N", "A");
    private static final BigDecimal MAX_DISCOUNT = new BigDecimal("99999.99");
    private static final int BATCH_SIZE = 200;

    private final PaymentRepository paymentRepository;
    private final BeneficiaryRepository beneficiaryRepository;

    PaymentImportService(PaymentRepository paymentRepository, BeneficiaryRepository beneficiaryRepository) {
        this.paymentRepository = paymentRepository;
        this.beneficiaryRepository = beneficiaryRepository;
    }

    /**
     * Executa a carga a partir dos arquivos de leiaute e de dados.
     *
     * @param layoutSource arquivo {@code layout-payment.txt}
     * @param dataSource arquivo {@code payment.dat}
     * @return relatório reconciliado da carga
     * @throws IOException se a leitura de qualquer um dos arquivos falhar
     */
    @Transactional
    public ImportReport<PaymentImportRejection> importFrom(
        InputStream layoutSource, InputStream dataSource) throws IOException {

        FixedWidthLayout layout = FixedWidthLayout.parse(layoutSource);
        List<LegacyPaymentRecord> records = new LegacyPaymentReader(layout).readAll(dataSource);

        List<ImportReport.RejectedRecord<PaymentImportRejection>> rejected = new ArrayList<>();
        List<Payment> pending = new ArrayList<>();
        Set<String> seenKeys = new HashSet<>();
        int skipped = 0;
        int loaded = 0;

        List<String> cpfs = records.stream().map(LegacyPaymentRecord::cpf).distinct().toList();
        Set<String> knownBeneficiaries = new HashSet<>(beneficiaryRepository.findExistingCpfs(cpfs));
        Set<String> existingKeys = new HashSet<>(paymentRepository.findExistingKeys(cpfs));

        for (LegacyPaymentRecord record : records) {
            String key = key(record.cpf(), record.referencePeriod());
            PaymentImportRejection rejection = validate(record, knownBeneficiaries, seenKeys, key);
            if (rejection != null) {
                rejected.add(new ImportReport.RejectedRecord<>(
                    record.lineNumber(), String.valueOf(record.paymentNumber()), rejection));
                continue;
            }
            seenKeys.add(key);
            // Idempotência pela chave única (cpf, reference_period): reexecutar a
            // carga ignora o que já existe em vez de violar a restrição.
            if (existingKeys.contains(key)) {
                skipped++;
                continue;
            }
            pending.add(toEntity(record));

            if (pending.size() >= BATCH_SIZE) {
                loaded += flush(pending);
            }
        }
        loaded += flush(pending);

        return new ImportReport<>(records.size(), loaded, skipped, rejected);
    }

    private int flush(List<Payment> pending) {
        if (pending.isEmpty()) {
            return 0;
        }
        paymentRepository.saveAll(pending);
        int written = pending.size();
        pending.clear();
        return written;
    }

    private PaymentImportRejection validate(
        LegacyPaymentRecord record,
        Set<String> knownBeneficiaries,
        Set<String> seenKeys,
        String key
    ) {
        if (!CpfValidator.isValid(record.cpf())) {
            return PaymentImportRejection.INVALID_CPF;
        }
        if (!knownBeneficiaries.contains(record.cpf())) {
            return PaymentImportRejection.UNKNOWN_BENEFICIARY;
        }
        if (!isValidPeriod(record.referencePeriod())) {
            return PaymentImportRejection.INVALID_PERIOD;
        }
        if (!isValidDate(record.generationDate())) {
            return PaymentImportRejection.INVALID_GENERATION_DATE;
        }
        if (record.programCode().isBlank()) {
            return PaymentImportRejection.EMPTY_PROGRAM;
        }
        if (!VALID_STATUSES.contains(record.status())) {
            return PaymentImportRejection.INVALID_STATUS;
        }
        if (!VALID_PAYMENT_TYPES.contains(record.paymentType())) {
            return PaymentImportRejection.INVALID_PAYMENT_TYPE;
        }
        if (isNegative(record.grossAmount())
            || isNegative(record.netAmount())
            || isNegative(record.discountTotal())
            || isNegative(record.bonusAmount())) {
            return PaymentImportRejection.NEGATIVE_AMOUNT;
        }
        // A origem declara AMT-DISC-TOTAL como P 7,2 e a coluna é NUMERIC(7,2):
        // um valor acima do limite seria truncado pelo banco em vez de recusado.
        if (record.discountTotal().compareTo(MAX_DISCOUNT) > 0) {
            return PaymentImportRejection.DISCOUNT_OUT_OF_RANGE;
        }
        if (seenKeys.contains(key)) {
            return PaymentImportRejection.DUPLICATE_PERIOD_IN_FILE;
        }
        return null;
    }

    private boolean isNegative(BigDecimal amount) {
        return amount.signum() < 0;
    }

    private boolean isValidPeriod(int yyyymm) {
        int month = yyyymm % 100;
        return yyyymm >= 100001 && yyyymm <= 999912 && month >= 1 && month <= 12;
    }

    private boolean isValidDate(int yyyymmdd) {
        if (yyyymmdd < 10000101 || yyyymmdd > 99991231) {
            return false;
        }
        try {
            LocalDate.of(yyyymmdd / 10000, yyyymmdd / 100 % 100, yyyymmdd % 100);
            return true;
        } catch (DateTimeException notADate) {
            return false;
        }
    }

    private String key(String cpf, int referencePeriod) {
        return cpf + '#' + referencePeriod;
    }

    private Payment toEntity(LegacyPaymentRecord record) {
        return Payment.migrated(
            record.cpf(),
            record.programCode(),
            record.referencePeriod(),
            record.grossAmount(),
            record.discountTotal(),
            record.netAmount(),
            record.bonusAmount(),
            toLocalDate(record.generationDate()),
            record.status(),
            record.paymentType());
    }

    private LocalDate toLocalDate(int yyyymmdd) {
        return LocalDate.of(yyyymmdd / 10000, yyyymmdd / 100 % 100, yyyymmdd % 100);
    }
}
