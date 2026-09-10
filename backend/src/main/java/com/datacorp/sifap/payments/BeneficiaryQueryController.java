package com.datacorp.sifap.payments;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Consulta de cadastro de beneficiário (REQ-034 a REQ-042).
 *
 * <p>O legado escolhe o critério por um campo de tela {@code #TYPE-SEARCH}
 * (CONSBENF.NSP:146-166). Aqui o critério é o parâmetro de consulta usado.
 */
@RestController
@RequestMapping("/api/v1/beneficiaries")
public class BeneficiaryQueryController {

    private final BeneficiaryQueryService beneficiaryQueryService;

    BeneficiaryQueryController(BeneficiaryQueryService beneficiaryQueryService) {
        this.beneficiaryQueryService = beneficiaryQueryService;
    }

    @GetMapping
    @Operation(summary = "Consultar beneficiário por CPF ou NIS")
    @ApiResponse(responseCode = "200", description = "Cadastro encontrado")
    @ApiResponse(responseCode = "400", description = "Critério de busca ausente ou ambíguo")
    @ApiResponse(responseCode = "404", description = "Beneficiário não encontrado")
    @ApiResponse(responseCode = "422", description = "CPF inválido")
    public BeneficiaryQueryResponse find(
        @RequestParam(required = false) String cpf,
        @RequestParam(required = false) Long nis
    ) {
        if (cpf == null && nis == null) {
            throw new BeneficiaryQuerySearchCriteriaException("Provide either cpf or nis");
        }
        if (cpf != null && nis != null) {
            throw new BeneficiaryQuerySearchCriteriaException("Provide only one of cpf or nis");
        }
        return cpf != null
            ? beneficiaryQueryService.findByCpf(cpf)
            : beneficiaryQueryService.findByNis(nis);
    }
}
