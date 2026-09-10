package com.datacorp.sifap.migration;

import java.math.BigDecimal;
import java.math.BigInteger;

/**
 * Decodificador de decimal compactado (BCD) do Adabas.
 *
 * <p>Cada byte carrega dois dígitos em nibbles de 4 bits, e o nibble menos
 * significativo do último byte é o sinal. Assim, um campo {@code P 9,2} ocupa
 * cinco bytes, não nove: nove dígitos mais o sinal, dois por byte.
 *
 * <p>O valor {@code 400,00} em {@code P 9,2} é escalado para 40000, alinhado à
 * direita em nove dígitos como {@code 000040000} e gravado como
 * {@code 0x00 0x00 0x40 0x00 0x0C}.
 *
 * <p>Convenção de sinal do Adabas: {@code C}, {@code A}, {@code E} e {@code F}
 * são positivos; {@code D} e {@code B} são negativos. Qualquer outro nibble
 * indica dado corrompido e é rejeitado — nunca convertido em zero, porque um
 * valor monetário silenciosamente zerado é indistinguível de um benefício
 * legitimamente nulo.
 */
public final class PackedDecimalDecoder {

    private PackedDecimalDecoder() {
    }

    /**
     * Decodifica um campo compactado.
     *
     * @param source registro completo
     * @param offset deslocamento do campo, em bytes
     * @param width largura do campo, em bytes
     * @param scale número de casas decimais declaradas no leiaute
     * @return valor com a escala declarada, preservando o sinal
     * @throws IllegalArgumentException se algum nibble estiver fora do
     *     alfabeto BCD ou se o campo ultrapassar o registro
     */
    public static BigDecimal decode(byte[] source, int offset, int width, int scale) {
        if (width < 1) {
            throw new IllegalArgumentException("Campo compactado precisa de ao menos 1 byte");
        }
        if (offset < 0 || offset + width > source.length) {
            throw new IllegalArgumentException(
                "Campo compactado fora dos limites do registro: offset=%d width=%d tamanho=%d"
                    .formatted(offset, width, source.length));
        }

        StringBuilder digits = new StringBuilder(width * 2);
        for (int i = 0; i < width; i++) {
            int current = source[offset + i] & 0xFF;
            int high = current >>> 4;
            int low = current & 0x0F;

            digits.append(requireDigit(high, offset + i));

            boolean isLastByte = i == width - 1;
            if (isLastByte) {
                return new BigDecimal(new BigInteger(digits.toString()), scale)
                    .multiply(signOf(low, offset + i));
            }
            digits.append(requireDigit(low, offset + i));
        }
        throw new IllegalStateException("inalcançável");
    }

    private static char requireDigit(int nibble, int position) {
        if (nibble > 9) {
            throw new IllegalArgumentException(
                "Nibble inválido 0x%X na posição %d: esperado dígito BCD".formatted(nibble, position));
        }
        return (char) ('0' + nibble);
    }

    private static BigDecimal signOf(int nibble, int position) {
        return switch (nibble) {
            case 0x0C, 0x0A, 0x0E, 0x0F -> BigDecimal.ONE;
            case 0x0D, 0x0B -> BigDecimal.valueOf(-1);
            default -> throw new IllegalArgumentException(
                "Nibble de sinal inválido 0x%X na posição %d".formatted(nibble, position));
        };
    }
}
