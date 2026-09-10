package com.datacorp.sifap.payments;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/payments/monthly-generations")
public class PaymentGenerationController {

    private final PaymentGenerationService paymentGenerationService;

    PaymentGenerationController(PaymentGenerationService paymentGenerationService) {
        this.paymentGenerationService = paymentGenerationService;
    }

    @PostMapping
    @Operation(summary = "Gerar pagamento mensal de beneficiário")
    @ApiResponse(responseCode = "201", description = "Pagamento criado")
    @ApiResponse(responseCode = "200", description = "Beneficiário ignorado sem criar pagamento")
    @ApiResponse(responseCode = "400", description = "Solicitação inválida")
    @ApiResponse(responseCode = "404", description = "Beneficiário ou programa não encontrado")
    @ApiResponse(responseCode = "422", description = "CPF ou período inválido")
    public ResponseEntity<PaymentGenerationResponse> generate(@Valid @RequestBody PaymentGenerationRequest request) {
        PaymentGenerationResponse response = paymentGenerationService.generate(request);
        if ("GENERATED".equals(response.outcome())) {
            return ResponseEntity.status(HttpStatus.CREATED).body(response);
        }
        if ("REJECTED".equals(response.outcome())) {
            return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY).body(response);
        }
        return ResponseEntity.ok(response);
    }

    public record PaymentGenerationRequest(
        @NotBlank @Pattern(regexp = "\\d{11}") String cpf,
        @NotNull Integer period
    ) {
    }
}
