package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class CpfValidatorTest {

    @Test
    void should_accept_valid_cpf_when_digits_match() {
        // REQ-003
        assertTrue(CpfValidator.isValid("52998224725"));
    }

    @Test
    void should_reject_invalid_cpf_when_digits_do_not_match() {
        // REQ-003
        assertFalse(CpfValidator.isValid("52998224724"));
    }

    @Test
    void should_reject_invalid_cpf_when_digits_are_repeated() {
        // REQ-003
        assertFalse(CpfValidator.isValid("00000000000"));
    }
}
