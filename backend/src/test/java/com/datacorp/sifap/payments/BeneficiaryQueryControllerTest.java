package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;

import org.junit.jupiter.api.Test;

class BeneficiaryQueryControllerTest {

    private final BeneficiaryQueryService service = mock(BeneficiaryQueryService.class);
    private final BeneficiaryQueryController controller = new BeneficiaryQueryController(service);

    @Test
    void should_route_to_cpf_search_when_only_cpf_is_provided() {
        // REQ-034 — o critério vem do parâmetro usado, substituindo o campo de
        // tela #TYPE-SEARCH do legado (CONSBENF.NSP:146-166).
        controller.find("52998224725", null);

        verify(service).findByCpf("52998224725");
    }

    @Test
    void should_route_to_nis_search_when_only_nis_is_provided() {
        // REQ-035
        controller.find(null, 700100200L);

        verify(service).findByNis(700100200L);
    }

    @Test
    void should_reject_request_without_search_criteria() {
        // REQ-034, REQ-035 — o legado recusa o tipo de busca desconhecido com
        // REINPUT 'INVALID SEARCH TYPE' (CONSBENF.NSP:165).
        assertAll(
            () -> assertThrows(
                BeneficiaryQuerySearchCriteriaException.class,
                () -> controller.find(null, null)),
            () -> verifyNoInteractions(service)
        );
    }

    @Test
    void should_reject_request_with_two_search_criteria() {
        // REQ-034, REQ-035 — o legado escolhe um único ramo do DECIDE; aceitar
        // ambos exigiria decidir silenciosamente qual prevalece.
        assertAll(
            () -> assertThrows(
                BeneficiaryQuerySearchCriteriaException.class,
                () -> controller.find("52998224725", 700100200L)),
            () -> verifyNoInteractions(service)
        );
    }
}
