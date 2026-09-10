package com.datacorp.sifap.payments;

import java.time.Clock;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Recalcula e persiste o total de descontos de um pagamento existente.
 *
 * <p>Reproduz o papel de {@code CALCDSCT.NSP}, que no legado é um programa
 * separado: lê um pagamento já gerado, apura os descontos registrados e
 * atualiza {@code AMT-DISC-TOTAL}.
 *
 * <p>Manter este caso de uso separado da geração mensal preserva a estrutura
 * do legado e evita antecipar a decisão registrada em {@code SIFAP-M-09}.
 */
@Service
class DiscountApplicationService {

    private final PaymentRepository paymentRepository;
    private final PaymentDiscountRepository paymentDiscountRepository;
    private final DiscountCalculationService discountCalculationService;
    private final Clock clock;

    @Autowired
    DiscountApplicationService(
        PaymentRepository paymentRepository,
        PaymentDiscountRepository paymentDiscountRepository,
        DiscountCalculationService discountCalculationService
    ) {
        this(paymentRepository, paymentDiscountRepository, discountCalculationService, Clock.systemDefaultZone());
    }

    DiscountApplicationService(
        PaymentRepository paymentRepository,
        PaymentDiscountRepository paymentDiscountRepository,
        DiscountCalculationService discountCalculationService,
        Clock clock
    ) {
        this.paymentRepository = paymentRepository;
        this.paymentDiscountRepository = paymentDiscountRepository;
        this.discountCalculationService = discountCalculationService;
        this.clock = clock;
    }

    @Transactional
    DiscountApplicationResponse apply(UUID paymentId) {
        Payment payment = paymentRepository.findById(paymentId)
            .orElseThrow(() -> new PaymentGenerationNotFoundException("Payment not found"));

        List<PaymentDiscount> discounts =
            paymentDiscountRepository.findByPaymentIdOrderBySequenceNumberAsc(paymentId);

        Money total = discountCalculationService.totalFor(
            new Money(payment.grossAmount()), discounts, currentDateAsNumber());

        payment.applyDiscountTotal(total);
        paymentRepository.save(payment);

        return DiscountApplicationResponse.of(payment, discounts.size());
    }

    /** Converte a data corrente para o formato {@code YYYYMMDD} usado pelo legado. */
    private int currentDateAsNumber() {
        LocalDate today = LocalDate.now(clock);
        return today.getYear() * 10_000 + today.getMonthValue() * 100 + today.getDayOfMonth();
    }
}
