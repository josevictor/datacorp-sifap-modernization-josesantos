package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class CpfMaskTest {

    @Test
    void should_reveal_only_the_last_five_digits() {
        // REQ-037 / AC-037.1
        assertEquals("***.***.247-25", CpfMask.of("52998224725"));
    }

    @ParameterizedTest
    @CsvSource({"52998224725", "11144477735", "39053344705"})
    void should_never_expose_the_first_six_digits(String cpf) {
        // REQ-037 / AC-037.2
        String masked = CpfMask.of(cpf);

        assertAll(
            () -> assertFalse(masked.contains(cpf.substring(0, 3)),
                () -> "Máscara expôs os três primeiros dígitos: " + masked),
            () -> assertFalse(masked.contains(cpf.substring(3, 6)),
                () -> "Máscara expôs o segundo bloco: " + masked),
            () -> assertEquals("***.***.", masked.substring(0, 8))
        );
    }

    @Test
    void should_reject_cpf_shorter_than_eleven_digits_instead_of_revealing_the_first_digits() {
        // REQ-037 — divergência deliberada. O legado tem um segundo ramo em
        // CONSBENF.NSP:298-301 que, para CPF com menos de 11 dígitos, revela
        // os TRÊS PRIMEIROS dígitos. Como as duas máscaras protegem partes
        // diferentes do documento, quem visse ambas reconstruiria o CPF.
        // O ramo não é replicado: a entrada inválida falha em vez de vazar.
        assertThrows(IllegalArgumentException.class, () -> CpfMask.of("5299822472"));
    }

    @Test
    void should_reject_null_cpf() {
        // REQ-037
        assertThrows(IllegalArgumentException.class, () -> CpfMask.of(null));
    }
}
