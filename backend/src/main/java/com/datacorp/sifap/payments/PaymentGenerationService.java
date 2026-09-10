package com.datacorp.sifap.payments;

import java.time.Clock;
import java.time.LocalDate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
class PaymentGenerationService {

    private final BeneficiaryRepository beneficiaryRepository;
    private final SocialProgramRepository socialProgramRepository;
    private final PaymentRepository paymentRepository;
    private final PaymentRejectionRepository paymentRejectionRepository;
    private final PaymentCalculationService paymentCalculationService;
    private final EligibilityValidationService eligibilityValidationService;
    private final Clock clock;

    @Autowired
    PaymentGenerationService(
        BeneficiaryRepository beneficiaryRepository,
        SocialProgramRepository socialProgramRepository,
        PaymentRepository paymentRepository,
        PaymentRejectionRepository paymentRejectionRepository,
        PaymentCalculationService paymentCalculationService,
        EligibilityValidationService eligibilityValidationService
    ) {
        this(
            beneficiaryRepository,
            socialProgramRepository,
            paymentRepository,
            paymentRejectionRepository,
            paymentCalculationService,
            eligibilityValidationService,
            Clock.systemDefaultZone());
    }

    PaymentGenerationService(
        BeneficiaryRepository beneficiaryRepository,
        SocialProgramRepository socialProgramRepository,
        PaymentRepository paymentRepository,
        PaymentRejectionRepository paymentRejectionRepository,
        PaymentCalculationService paymentCalculationService,
        EligibilityValidationService eligibilityValidationService,
        Clock clock
    ) {
        this.beneficiaryRepository = beneficiaryRepository;
        this.socialProgramRepository = socialProgramRepository;
        this.paymentRepository = paymentRepository;
        this.paymentRejectionRepository = paymentRejectionRepository;
        this.paymentCalculationService = paymentCalculationService;
        this.eligibilityValidationService = eligibilityValidationService;
        this.clock = clock;
    }

    @Transactional
    PaymentGenerationResponse generate(PaymentGenerationController.PaymentGenerationRequest request) {
        YearMonthPeriod period = YearMonthPeriod.of(request.period());
        if (!CpfValidator.isValid(request.cpf())) {
            paymentRejectionRepository.save(PaymentRejection.of(
                request.cpf(), period, "INVALID_CPF", java.time.OffsetDateTime.now(clock)));
            return PaymentGenerationResponse.rejected("INVALID_CPF");
        }

        Beneficiary beneficiary = beneficiaryRepository.findByCpf(request.cpf())
            .orElseThrow(() -> new PaymentGenerationNotFoundException("Beneficiary not found"));

        if (!beneficiary.isActive()) {
            return PaymentGenerationResponse.ignored("BENEFICIARY_NOT_ACTIVE");
        }

        if (paymentRepository.existsByCpfAndReferencePeriod(beneficiary.cpf(), period.value())) {
            return PaymentGenerationResponse.ignored("PAYMENT_ALREADY_GENERATED");
        }

        SocialProgram program = socialProgramRepository.findByCode(beneficiary.programCode())
            .orElseThrow(() -> new PaymentGenerationNotFoundException("Program not found"));

        if (!program.isActive()) {
            return PaymentGenerationResponse.ignored("PROGRAM_NOT_ACTIVE");
        }

        // REQ-033 — espelha o CALLNAT 'VALELEG' de BATCHPGT.NSP:369-379, entre
        // a validação de CPF e o cálculo. O beneficiário inelegível é ignorado,
        // não rejeitado: o legado o contabiliza em #QTY-IGNORED.
        EligibilityStatus eligibility = eligibilityValidationService.validate(beneficiary, program, period);
        if (!eligibility.isEligible()) {
            return PaymentGenerationResponse.ignored(eligibility.reason()
                .map(Enum::name)
                .orElse("NOT_ELIGIBLE"));
        }

        PaymentCalculation calculation = paymentCalculationService.calculate(beneficiary, program, period);
        Payment payment = Payment.generated(
            beneficiary.cpf(),
            beneficiary.programCode(),
            period,
            calculation,
            LocalDate.now(clock));

        return PaymentGenerationResponse.generated(paymentRepository.save(payment));
    }
}
