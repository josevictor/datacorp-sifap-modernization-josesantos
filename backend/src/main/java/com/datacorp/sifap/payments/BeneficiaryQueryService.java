package com.datacorp.sifap.payments;

import java.time.Clock;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Limit;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Consulta de cadastro de beneficiário (REQ-034 a REQ-042).
 *
 * <p>Moderniza a transação online {@code CONSBENF.NSP}.
 */
@Service
class BeneficiaryQueryService {

    /** Corte do histórico, conforme CONSBENF.NSP:277-279 (REQ-039). */
    private static final int HISTORY_LIMIT = 12;

    private final BeneficiaryRepository beneficiaryRepository;
    private final PaymentRepository paymentRepository;
    private final AuditTrailRepository auditTrailRepository;
    private final Clock clock;

    @Autowired
    BeneficiaryQueryService(
        BeneficiaryRepository beneficiaryRepository,
        PaymentRepository paymentRepository,
        AuditTrailRepository auditTrailRepository
    ) {
        this(beneficiaryRepository, paymentRepository, auditTrailRepository, Clock.systemDefaultZone());
    }

    BeneficiaryQueryService(
        BeneficiaryRepository beneficiaryRepository,
        PaymentRepository paymentRepository,
        AuditTrailRepository auditTrailRepository,
        Clock clock
    ) {
        this.beneficiaryRepository = beneficiaryRepository;
        this.paymentRepository = paymentRepository;
        this.auditTrailRepository = auditTrailRepository;
        this.clock = clock;
    }

    /**
     * Consulta pelo CPF (REQ-034).
     *
     * <p>O CPF é validado antes de qualquer acesso ao cadastro, espelhando o
     * {@code CALLNAT 'SUBVALCP'} que antecede o {@code FIND} em
     * {@code CONSBENF.NSP:132-144} (REQ-036).
     */
    @Transactional
    BeneficiaryQueryResponse findByCpf(String cpf) {
        if (!CpfValidator.isValid(cpf)) {
            throw new BeneficiaryQueryRejectedException("Invalid CPF");
        }
        return respond(beneficiaryRepository.findByCpf(cpf));
    }

    /**
     * Consulta pelo NIS (REQ-035).
     *
     * <p>O NIS não é validado antes da busca: no legado, {@code SUBVALCP} só é
     * acionado no ramo de CPF. O comportamento é preservado.
     */
    @Transactional
    BeneficiaryQueryResponse findByNis(long nis) {
        return respond(beneficiaryRepository.findByNis(nis));
    }

    private BeneficiaryQueryResponse respond(Optional<Beneficiary> found) {
        Beneficiary beneficiary = found
            .orElseThrow(() -> new BeneficiaryQueryNotFoundException("Beneficiary not found"));

        List<Payment> history = paymentRepository.findByCpfOrderByReferencePeriodDesc(
            beneficiary.cpf(), Limit.of(HISTORY_LIMIT));

        // REQ-042 — a trilha só é gravada no caminho de sucesso. No legado, o
        // beneficiário não encontrado provoca REINPUT, que reinicia o laço
        // antes de alcançar o bloco de auditoria (CONSBENF.NSP:168-179).
        auditTrailRepository.save(AuditTrail.beneficiaryQuery(
            beneficiary.cpf(), OffsetDateTime.now(clock)));

        return BeneficiaryQueryResponse.of(beneficiary, history);
    }
}
