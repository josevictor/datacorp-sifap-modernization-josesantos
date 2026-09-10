package com.datacorp.sifap.migration;

import com.datacorp.sifap.migration.FixedWidthLayout.LayoutField;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;

/**
 * Um registro de largura fixa já posicionado sobre seu leiaute.
 *
 * <p>Os campos são lidos pelo nome legado, e não por deslocamento literal, para
 * que a posição venha sempre do leiaute declarado.
 *
 * @param raw bytes do registro, sem o separador
 * @param layout leiaute que descreve o registro
 * @param lineNumber posição no arquivo, em base 1
 */
public record FixedWidthRecord(byte[] raw, FixedWidthLayout layout, long lineNumber) {

    /**
     * Lê um campo alfanumérico, removendo o preenchimento.
     *
     * @param name nome legado do campo
     * @return conteúdo do campo sem espaços nas extremidades
     */
    public String text(String name) {
        LayoutField field = layout.field(name);
        // ISO-8859-1 mapeia cada byte a um caractere, então nenhum byte da
        // extração é substituído silenciosamente por um marcador de erro.
        return new String(raw, field.offset(), field.width(), StandardCharsets.ISO_8859_1).trim();
    }

    /**
     * Lê um campo numérico em ASCII.
     *
     * @param name nome legado do campo
     * @return valor do campo; {@code 0} quando em branco
     * @throws IllegalArgumentException se o conteúdo não for numérico, o que
     *     costuma indicar deslocamento de leiaute
     */
    public long number(String name) {
        String content = text(name);
        if (content.isEmpty()) {
            return 0L;
        }
        try {
            return Long.parseLong(content);
        } catch (NumberFormatException cause) {
            throw new IllegalArgumentException(
                "Campo %s não é numérico na linha %d: \"%s\"".formatted(name, lineNumber, content), cause);
        }
    }

    /**
     * Lê um campo decimal compactado.
     *
     * @param name nome legado do campo
     * @return valor decodificado, na escala declarada pelo leiaute
     */
    public BigDecimal packed(String name) {
        LayoutField field = layout.field(name);
        return PackedDecimalDecoder.decode(raw, field.offset(), field.width(), field.scale());
    }
}
