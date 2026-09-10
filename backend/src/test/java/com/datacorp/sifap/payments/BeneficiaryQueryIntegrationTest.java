package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Transactional
class BeneficiaryQueryIntegrationTest {

    private static final String CPF = "52998224725";

    @Autowired
    private BeneficiaryRepository beneficiaryRepository;

    @Autowired
    private PaymentRepository paymentRepository;

    @Autowired
    private AuditTrailRepository auditTrailRepository;

    @Autowired
    private BeneficiaryQueryService beneficiaryQueryService;

    @Test
    void should_return_registration_when_cpf_is_registered() {
        // REQ-034 / AC-034.1
        beneficiaryRepository.save(beneficiary(CPF, 700100200L, "A"));

        BeneficiaryQueryResponse response = beneficiaryQueryService.findByCpf(CPF);

        assertAll(
            () -> assertEquals("***.***.247-25", response.maskedCpf()),
            () -> assertEquals("Pessoa Beneficiaria", response.fullName()),
            () -> assertEquals("A", response.statusCode()),
            () -> assertEquals("Ativo", response.statusDescription()),
            () -> assertEquals(700100200L, response.nis())
        );
    }

    @Test
    void should_report_not_found_when_valid_cpf_is_not_registered() {
        // REQ-034 / AC-034.2
        assertThrows(
            BeneficiaryQueryNotFoundException.class,
            () -> beneficiaryQueryService.findByCpf("11144477735"));
    }

    @Test
    void should_return_registration_when_nis_is_registered() {
        // REQ-035 / AC-035.1
        beneficiaryRepository.save(beneficiary(CPF, 700100200L, "S"));

        BeneficiaryQueryResponse response = beneficiaryQueryService.findByNis(700100200L);

        assertAll(
            () -> assertEquals("***.***.247-25", response.maskedCpf()),
            () -> assertEquals("Suspenso", response.statusDescription())
        );
    }

    @Test
    void should_report_not_found_when_nis_is_not_registered() {
        // REQ-035 / AC-035.2 — o NIS não é validado antes da busca, porque o
        // legado só aciona SUBVALCP no ramo de CPF (CONSBENF.NSP:132-163).
        assertThrows(
            BeneficiaryQueryNotFoundException.class,
            () -> beneficiaryQueryService.findByNis(999999999L));
    }

    @Test
    void should_reject_invalid_cpf_without_reading_the_registration() {
        // REQ-036 / AC-036.1 e AC-036.2 — o CPF 52998224724 tem o último
        // dígito verificador errado. O cadastro existe sob o CPF válido, e a
        // rejeição não pode alcançá-lo.
        beneficiaryRepository.save(beneficiary(CPF, 700100200L, "A"));

        assertAll(
            () -> assertThrows(
                BeneficiaryQueryRejectedException.class,
                () -> beneficiaryQueryService.findByCpf("52998224724")),
            () -> assertEquals(0, auditTrailRepository.count(),
                () -> "Consulta rejeitada não deve gravar trilha nem tocar o cadastro")
        );
    }

    @Test
    void should_limit_history_to_twelve_payments() {
        // REQ-039 / AC-039.1
        beneficiaryRepository.save(beneficiary(CPF, 700100200L, "A"));
        savePayments(202501, 15);

        BeneficiaryQueryResponse response = beneficiaryQueryService.findByCpf(CPF);

        assertEquals(12, response.paymentHistory().size());
    }

    @Test
    void should_return_all_payments_when_there_are_fewer_than_twelve() {
        // REQ-039 / AC-039.2
        beneficiaryRepository.save(beneficiary(CPF, 700100200L, "A"));
        savePayments(202601, 5);

        BeneficiaryQueryResponse response = beneficiaryQueryService.findByCpf(CPF);

        assertEquals(5, response.paymentHistory().size());
    }

    @Test
    void should_order_history_from_most_recent_to_oldest() {
        // REQ-040 / AC-040.1 — os pagamentos são gravados fora de ordem
        // cronológica de propósito. O legado leria na ordem do descritor de
        // CPF, sem ordenar por período (CONSBENF.NSP:270-284).
        beneficiaryRepository.save(beneficiary(CPF, 700100200L, "A"));
        savePayment(202601);
        savePayment(202603);
        savePayment(202602);

        BeneficiaryQueryResponse response = beneficiaryQueryService.findByCpf(CPF);

        assertEquals(
            List.of(202603, 202602, 202601),
            response.paymentHistory().stream()
                .map(BeneficiaryQueryResponse.PaymentHistoryEntry::referencePeriod)
                .toList());
    }

    @Test
    void should_keep_the_twelve_most_recent_periods_when_history_is_truncated() {
        // REQ-040 / AC-040.2 — é este o caso que o legado erra: com quinze
        // pagamentos, o corte no décimo segundo registro lido pode descartar
        // justamente os mais recentes.
        beneficiaryRepository.save(beneficiary(CPF, 700100200L, "A"));
        savePayments(202501, 15);

        BeneficiaryQueryResponse response = beneficiaryQueryService.findByCpf(CPF);

        List<Integer> periods = response.paymentHistory().stream()
            .map(BeneficiaryQueryResponse.PaymentHistoryEntry::referencePeriod)
            .toList();

        assertAll(
            () -> assertEquals(202603, periods.getFirst()),
            () -> assertEquals(202504, periods.getLast())
        );
    }

    @Test
    void should_report_absence_of_payments_explicitly() {
        // REQ-041 / AC-041.1
        beneficiaryRepository.save(beneficiary(CPF, 700100200L, "A"));

        BeneficiaryQueryResponse response = beneficiaryQueryService.findByCpf(CPF);

        assertAll(
            () -> assertTrue(response.paymentHistory().isEmpty()),
            () -> assertTrue(response.hasNoPayments())
        );
    }

    @Test
    void should_record_audit_trail_when_query_succeeds() {
        // REQ-042 / AC-042.1
        beneficiaryRepository.save(beneficiary(CPF, 700100200L, "A"));

        beneficiaryQueryService.findByCpf(CPF);

        AuditTrail trail = auditTrailRepository.findAll().getFirst();
        assertAll(
            () -> assertEquals(1, auditTrailRepository.count()),
            () -> assertEquals("CO", trail.actionCode()),
            () -> assertEquals("BENF", trail.entityType()),
            () -> assertEquals(CPF, trail.affectedCpf())
        );
    }

    @Test
    void should_not_record_audit_trail_when_beneficiary_is_not_found() {
        // REQ-042 / AC-042.2 — no legado, o beneficiário não encontrado
        // provoca REINPUT, que reinicia o laço antes do bloco de auditoria.
        assertThrows(
            BeneficiaryQueryNotFoundException.class,
            () -> beneficiaryQueryService.findByCpf("11144477735"));

        assertEquals(0, auditTrailRepository.count());
    }

    @Test
    void should_report_not_found_when_nis_is_zero_even_with_many_such_records() {
        // REQ-035 — regressão. O zero é o padrão da coluna `nis` desde a
        // migração V5, então vários beneficiários o compartilham. Sem a guarda
        // no serviço, `findByNis(0)` casaria com todos e a consulta falharia
        // com erro de resultado múltiplo em vez de responder "não encontrado".
        //
        // A guarda reproduz o Adabas: `AM NUM-NIS` é DE,UQ,NU, e a supressão
        // de nulos mantém os registros sem NIS fora do índice — um FIND por
        // vazio não retorna nada.
        beneficiaryRepository.save(beneficiary(CPF, 0L, "A"));
        beneficiaryRepository.save(beneficiary("11144477735", 0L, "A"));

        assertThrows(
            BeneficiaryQueryNotFoundException.class,
            () -> beneficiaryQueryService.findByNis(0L));
    }

    private Beneficiary beneficiary(String cpf, long nis, String status) {
        return new Beneficiary(
            UUID.randomUUID(), cpf, "Pessoa Beneficiaria", 19800101, status, "P001",
            new BigDecimal("100.00"), 0, "15", nis, "S");
    }

    private void savePayments(int firstPeriod, int count) {
        int year = firstPeriod / 100;
        int month = firstPeriod % 100;
        for (int index = 0; index < count; index++) {
            savePayment(year * 100 + month);
            month++;
            if (month > 12) {
                month = 1;
                year++;
            }
        }
    }

    private void savePayment(int period) {
        PaymentCalculation calculation = new PaymentCalculation(
            new Money(new BigDecimal("100.00")),
            Money.zero(),
            Money.zero(),
            new Money(new BigDecimal("100.00")),
            "N");
        paymentRepository.save(Payment.generated(
            CPF, "P001", YearMonthPeriod.of(period), calculation, LocalDate.of(2026, 1, 10)));
    }
}
