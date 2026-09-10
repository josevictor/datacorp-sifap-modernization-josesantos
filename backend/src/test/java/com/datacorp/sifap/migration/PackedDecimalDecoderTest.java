package com.datacorp.sifap.migration;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class PackedDecimalDecoderTest {

    @Test
    void should_decode_the_documented_sample_of_four_hundred() {
        // 400,00 em P 9,2 é escalado para 40000 e alinhado à direita em nove
        // dígitos: 000040000. O nibble 4 fica na quinta posição, não na sexta.
        byte[] raw = {0x00, 0x00, 0x40, 0x00, 0x0C};

        BigDecimal value = PackedDecimalDecoder.decode(raw, 0, 5, 2);

        assertAll(
            () -> assertEquals(new BigDecimal("400.00"), value),
            () -> assertEquals(2, value.scale()));
    }

    @Test
    void should_decode_zero_without_losing_the_declared_scale() {
        byte[] raw = {0x00, 0x00, 0x00, 0x00, 0x0C};

        BigDecimal value = PackedDecimalDecoder.decode(raw, 0, 5, 2);

        assertAll(
            () -> assertEquals(0, value.signum()),
            () -> assertEquals(new BigDecimal("0.00"), value));
    }

    @Test
    void should_decode_negative_values_from_the_sign_nibble() {
        byte[] raw = {0x00, 0x00, 0x15, 0x00, 0x0D};

        assertEquals(new BigDecimal("-150.00"), PackedDecimalDecoder.decode(raw, 0, 5, 2));
    }

    @Test
    void should_use_the_widest_value_that_fits_nine_digits() {
        byte[] raw = {(byte) 0x99, (byte) 0x99, (byte) 0x99, (byte) 0x99, (byte) 0x9C};

        assertEquals(new BigDecimal("9999999.99"), PackedDecimalDecoder.decode(raw, 0, 5, 2));
    }

    @Test
    void should_decode_only_the_requested_field_when_neighbours_are_present() {
        // Um deslocamento errado lê o campo vizinho e devolve um número plausível,
        // por isso o teste cerca o campo alvo com dados de outros campos.
        byte[] raw = {(byte) 0xFF, 0x00, 0x00, 0x40, 0x00, 0x0C, (byte) 0xFF};

        assertEquals(new BigDecimal("400.00"), PackedDecimalDecoder.decode(raw, 1, 5, 2));
    }

    @ParameterizedTest
    @CsvSource({"10", "11", "12", "13", "14", "15"})
    void should_reject_a_non_digit_nibble_instead_of_yielding_zero(int corruptedNibble) {
        byte[] raw = {(byte) (corruptedNibble << 4), 0x00, 0x00, 0x00, 0x0C};

        assertThrows(
            IllegalArgumentException.class,
            () -> PackedDecimalDecoder.decode(raw, 0, 5, 2));
    }

    @Test
    void should_reject_an_unknown_sign_nibble() {
        byte[] raw = {0x00, 0x00, 0x04, 0x00, 0x00};

        assertThrows(
            IllegalArgumentException.class,
            () -> PackedDecimalDecoder.decode(raw, 0, 5, 2));
    }

    @Test
    void should_reject_a_field_that_runs_past_the_record() {
        byte[] raw = {0x00, 0x00, 0x0C};

        assertThrows(
            IllegalArgumentException.class,
            () -> PackedDecimalDecoder.decode(raw, 0, 5, 2));
    }
}
