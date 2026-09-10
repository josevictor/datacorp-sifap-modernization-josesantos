package com.datacorp.sifap.migration;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Leiaute de largura fixa no estilo {@code ADACMP}, derivado do arquivo
 * {@code layout-beneficiary.txt} que acompanha a extração legada.
 *
 * <p>Os deslocamentos são calculados pela soma acumulada das larguras
 * declaradas, nunca informados manualmente. Um deslocamento incorreto não
 * gera exceção: ele lê o campo vizinho e produz um valor plausível e errado,
 * que é a falha mais perigosa de uma carga de largura fixa.
 *
 * <p>Cada linha útil tem oito colunas; linhas iniciadas por {@code #} são
 * comentários. A largura total derivada é conferida contra a linha
 * {@code # RECORD-BYTES N} do rodapé, quando presente.
 *
 * <pre>{@code
 * # LEVEL CODE NAME FORMAT LENGTH OCCURS OPTIONS BYTE-WIDTH
 * 01 CH AMT-FAMILY-INCOME            P 9,2   1   -          5
 * }</pre>
 */
public final class FixedWidthLayout {

    private static final String RECORD_BYTES_MARKER = "# RECORD-BYTES";
    private static final int EXPECTED_COLUMNS = 8;

    private final Map<String, LayoutField> fields;
    private final int recordWidth;

    private FixedWidthLayout(Map<String, LayoutField> fields, int recordWidth) {
        this.fields = fields;
        this.recordWidth = recordWidth;
    }

    /**
     * Interpreta um leiaute e devolve os campos já posicionados.
     *
     * @param source conteúdo do arquivo de leiaute; é totalmente consumido
     * @return leiaute com deslocamentos derivados das larguras declaradas
     * @throws IOException se a leitura falhar
     * @throws IllegalArgumentException se alguma linha for malformada ou se a
     *     soma das larguras divergir do total declarado no rodapé
     */
    public static FixedWidthLayout parse(InputStream source) throws IOException {
        Map<String, LayoutField> parsed = new LinkedHashMap<>();
        int offset = 0;
        Integer declaredWidth = null;

        try (BufferedReader reader =
                 new BufferedReader(new InputStreamReader(source, StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String trimmed = line.trim();
                if (trimmed.startsWith(RECORD_BYTES_MARKER)) {
                    declaredWidth = Integer.parseInt(trimmed.substring(RECORD_BYTES_MARKER.length()).trim());
                    continue;
                }
                if (trimmed.isEmpty() || trimmed.startsWith("#")) {
                    continue;
                }
                LayoutField field = parseField(trimmed, offset);
                if (parsed.put(field.name(), field) != null) {
                    throw new IllegalArgumentException("Campo duplicado no leiaute: " + field.name());
                }
                offset += field.width() * field.occurs();
            }
        }

        if (parsed.isEmpty()) {
            throw new IllegalArgumentException("Leiaute não declara nenhum campo");
        }
        // A conferência contra o rodapé é o que impede uma carga silenciosamente
        // deslocada quando o leiaute e o arquivo de dados saem de sincronia.
        if (declaredWidth != null && declaredWidth != offset) {
            throw new IllegalArgumentException(
                "Largura derivada (%d) diverge da declarada em RECORD-BYTES (%d)"
                    .formatted(offset, declaredWidth));
        }
        return new FixedWidthLayout(parsed, offset);
    }

    private static LayoutField parseField(String line, int offset) {
        String[] parts = line.split("\\s+");
        if (parts.length < EXPECTED_COLUMNS) {
            throw new IllegalArgumentException("Linha de leiaute com colunas insuficientes: " + line);
        }
        String name = parts[2];
        char format = parts[3].charAt(0);
        String length = parts[4];
        int occurs = Integer.parseInt(parts[5]);
        int totalWidth = Integer.parseInt(parts[7]);

        if (occurs < 1) {
            throw new IllegalArgumentException("OCCURS inválido para o campo " + name);
        }
        if (totalWidth % occurs != 0) {
            throw new IllegalArgumentException(
                "BYTE-WIDTH %d não é múltiplo de OCCURS %d no campo %s".formatted(totalWidth, occurs, name));
        }

        int commaAt = length.indexOf(',');
        int scale = commaAt < 0 ? 0 : Integer.parseInt(length.substring(commaAt + 1));

        return new LayoutField(name, format, offset, totalWidth / occurs, occurs, scale);
    }

    /**
     * Recupera um campo pelo nome legado.
     *
     * @param name nome exatamente como aparece no leiaute, por exemplo {@code NUM-CPF}
     * @return descrição posicionada do campo
     * @throws IllegalArgumentException se o campo não existir no leiaute
     */
    public LayoutField field(String name) {
        LayoutField field = fields.get(name);
        if (field == null) {
            throw new IllegalArgumentException("Campo ausente no leiaute: " + name);
        }
        return field;
    }

    /**
     * @return largura de um registro em bytes, sem o separador de linha
     */
    public int recordWidth() {
        return recordWidth;
    }

    /**
     * Campo posicionado dentro do registro.
     *
     * @param name nome legado do campo
     * @param format formato Adabas: {@code A}, {@code N} ou {@code P}
     * @param offset deslocamento em bytes a partir do início do registro
     * @param width largura de uma ocorrência, em bytes
     * @param occurs número de ocorrências para campos MU/PE
     * @param scale casas decimais declaradas, {@code 0} quando inteiro
     */
    public record LayoutField(String name, char format, int offset, int width, int occurs, int scale) {
    }
}
