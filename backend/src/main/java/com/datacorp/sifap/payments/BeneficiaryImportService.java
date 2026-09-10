package com.datacorp.sifap.payments;

import com.datacorp.sifap.migration.FixedWidthLayout;
import com.datacorp.sifap.migration.LegacyBeneficiaryReader;
import com.datacorp.sifap.migration.LegacyBeneficiaryRecord;
import java.io.IOException;
import java.io.InputStream;
import java.math.BigDecimal;
import java.time.DateTimeException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Carrega beneficiários da extração legada para o modelo moderno.
 *
 * <p>A carga é idempotente: um CPF já presente é ignorado, e não atualizado,
 * de modo que reexecutar a importação não altera dados existentes nem falha.
 *
 * <p>Só os campos consumidos pelo sistema moderno são migrados; os demais
 * permanecem na extração. Registros fora dos domínios conhecidos são recusados
 * com motivo em vez de carregados com valores corrigidos, porque adivinhar o
 * valor pretendido de um dado legado inválido cria uma verdade que nunca
 * existiu na origem.
 *
 * <p>Carregar um beneficiário não implica que ele seja elegível a pagamento: a
 * elegibilidade é avaliada depois, por {@link EligibilityValidationService},
 * segundo as regras legadas.
 */
@Service
public class BeneficiaryImportService {

    private static final Set<String> KNOWN_REGIONS = Set.of("01", "02", "03", "04", "05", "99");
    private static final Set<String> VALID_STATUSES = Set.of("A", "S", "C", "I", "D");
    private static final Set<String> VALID_DOCS_FLAGS = Set.of("S", "N");
    private static final int BATCH_SIZE = 100;

    private final BeneficiaryRepository beneficiaryRepository;

    BeneficiaryImportService(BeneficiaryRepository beneficiaryRepository) {
        this.beneficiaryRepository = beneficiaryRepository;
    }

    /**
     * Executa a carga a partir dos arquivos de leiaute e de dados.
     *
     * @param layoutSource arquivo {@code layout-beneficiary.txt}
     * @param dataSource arquivo {@code beneficiary.dat}
     * @return relatório reconciliado da carga
     * @throws IOException se a leitura de qualquer um dos arquivos falhar
     */    @Transactional
    public ImportReport<BeneficiaryImportRejection> importFrom(
        InputStream layoutSource, InputStream dataSource) throws IOException {

        FixedWidthLayout layout = FixedWidthLayout.parse(layoutSource);
        List<LegacyBeneficiaryRecord> records = new LegacyBeneficiaryReader(layout).readAll(dataSource);

        List<ImportReport.RejectedRecord<BeneficiaryImportRejection>> rejected = new ArrayList<>();
        List<Beneficiary> pending = new ArrayList<>();
        Set<String> seenCpfs = new HashSet<>();
        Set<Long> seenNis = new HashSet<>();
        int skipped = 0;
        int loaded = 0;

        Set<String> existingCpfs = new HashSet<>(
            beneficiaryRepository.findExistingCpfs(records.stream().map(LegacyBeneficiaryRecord::cpf).toList()));
        Set<Long> existingNis = new HashSet<>(
            beneficiaryRepository.findExistingNis(records.stream().map(LegacyBeneficiaryRecord::nis).toList()));
        // NIS já gravados disputam a unicidade junto com os do arquivo, para que
        // uma colisão contra a base seja detectada antes do banco recusá-la.
        seenNis.addAll(existingNis);

        for (LegacyBeneficiaryRecord record : records) {
            BeneficiaryImportRejection rejection = validate(record, seenCpfs);
            if (rejection != null) {
                rejected.add(new ImportReport.RejectedRecord<>(
                    record.lineNumber(), record.registration(), rejection));
                continue;
            }
            // A idempotência é decidida antes da unicidade do NIS: um registro já
            // carregado colide com a própria linha na base, e tratá-lo como
            // duplicidade transformaria toda reexecução em 500 recusas.
            if (!existingCpfs.add(record.cpf())) {
                seenCpfs.add(record.cpf());
                skipped++;
                continue;
            }
            seenCpfs.add(record.cpf());
            if (record.nis() > 0 && !seenNis.add(record.nis())) {
                rejected.add(new ImportReport.RejectedRecord<>(
                    record.lineNumber(), record.registration(), BeneficiaryImportRejection.DUPLICATE_NIS));
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

    private int flush(List<Beneficiary> pending) {
        if (pending.isEmpty()) {
            return 0;
        }
        beneficiaryRepository.saveAll(pending);
        int written = pending.size();
        pending.clear();
        return written;
    }

    private BeneficiaryImportRejection validate(
        LegacyBeneficiaryRecord record,
        Set<String> seenCpfs
    ) {
        if (!CpfValidator.isValid(record.cpf())) {
            return BeneficiaryImportRejection.INVALID_CPF;
        }
        if (seenCpfs.contains(record.cpf())) {
            return BeneficiaryImportRejection.DUPLICATE_CPF_IN_FILE;
        }
        if (record.fullName().isBlank()) {
            return BeneficiaryImportRejection.EMPTY_NAME;
        }
        if (!isValidDate(record.birthDate())) {
            return BeneficiaryImportRejection.INVALID_BIRTH_DATE;
        }
        if (!KNOWN_REGIONS.contains(record.regionCode())) {
            return BeneficiaryImportRejection.UNKNOWN_REGION;
        }
        if (record.programCode().isBlank()) {
            return BeneficiaryImportRejection.EMPTY_PROGRAM;
        }
        if (!VALID_STATUSES.contains(record.status())) {
            return BeneficiaryImportRejection.INVALID_STATUS;
        }
        if (record.familyIncome().signum() < 0) {
            return BeneficiaryImportRejection.NEGATIVE_INCOME;
        }
        if (record.dependentCount() < 0) {
            return BeneficiaryImportRejection.NEGATIVE_DEPENDENTS;
        }
        if (!VALID_DOCS_FLAGS.contains(record.docsOk())) {
            return BeneficiaryImportRejection.INVALID_DOCS_FLAG;
        }
        // A unicidade do NIS não é avaliada aqui: ela depende do que já foi
        // aceito nesta execução e do que existe na base, e precisa ocorrer
        // depois da decisão de idempotência.
        return null;
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

    private Beneficiary toEntity(LegacyBeneficiaryRecord record) {
        BigDecimal income = record.familyIncome().setScale(2);
        return new Beneficiary(
            UUID.randomUUID(),
            record.cpf(),
            record.fullName(),
            record.birthDate(),
            record.status(),
            record.programCode(),
            income,
            record.dependentCount(),
            record.regionCode(),
            record.nis(),
            record.docsOk());
    }
}
