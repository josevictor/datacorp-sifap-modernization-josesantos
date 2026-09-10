package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

class BeneficiaryStatusDescriptionTest {

    @ParameterizedTest
    @CsvSource({
        "A, Ativo",
        "S, Suspenso",
        "C, Cancelado",
        "I, Inativo",
        "D, Encerrado"
    })
    void should_describe_each_known_status(String code, String expected) {
        // REQ-038 / AC-038.1 e AC-038.2
        assertEquals(expected, BeneficiaryStatusDescription.of(code));
    }

    @ParameterizedTest
    @ValueSource(strings = {"X", "", " ", "a"})
    void should_describe_unknown_status_instead_of_failing(String code) {
        // REQ-038 / AC-038.3 — espelha o ramo NONE do DECIDE em
        // CONSBENF.NSP:239-240.
        assertEquals("Desconhecido", BeneficiaryStatusDescription.of(code));
    }
}
