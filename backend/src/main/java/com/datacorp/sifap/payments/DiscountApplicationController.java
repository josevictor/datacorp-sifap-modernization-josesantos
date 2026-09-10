package com.datacorp.sifap.payments;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import java.util.UUID;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/payments/{paymentId}/discount-calculations")
public class DiscountApplicationController {

    private final DiscountApplicationService discountApplicationService;

    DiscountApplicationController(DiscountApplicationService discountApplicationService) {
        this.discountApplicationService = discountApplicationService;
    }

    @PostMapping
    @Operation(summary = "Recalcular os descontos de um pagamento existente")
    @ApiResponse(responseCode = "200", description = "Descontos recalculados")
    @ApiResponse(responseCode = "404", description = "Pagamento não encontrado")
    public ResponseEntity<DiscountApplicationResponse> apply(@PathVariable UUID paymentId) {
        return ResponseEntity.ok(discountApplicationService.apply(paymentId));
    }
}
