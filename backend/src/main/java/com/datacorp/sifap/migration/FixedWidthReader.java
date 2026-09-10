package com.datacorp.sifap.migration;

import java.io.EOFException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

/**
 * Leitor de extrações legadas em largura fixa.
 *
 * <p>A leitura ocorre em blocos de exatamente {@link FixedWidthLayout#recordWidth()}
 * bytes mais o separador. Não se usa leitura por linha: campos compactados
 * contêm bytes como {@code 0x0C}, {@code 0x1C} e {@code 0x1D}, que várias APIs
 * de texto tratam como quebra de linha e que partiriam registros ao meio. Com
 * largura fixa, o conteúdo binário nunca influencia o enquadramento.
 */
public final class FixedWidthReader {

    private static final byte RECORD_SEPARATOR = '\n';

    private final FixedWidthLayout layout;

    public FixedWidthReader(FixedWidthLayout layout) {
        this.layout = layout;
    }

    /**
     * Lê a extração inteira, convertendo cada registro.
     *
     * @param source arquivo de dados; é totalmente consumido
     * @param mapper conversão de um registro posicionado no tipo de destino
     * @param <T> tipo de destino
     * @return registros na ordem do arquivo
     * @throws IOException se a leitura falhar ou se os registros perderem alinhamento
     * @throws EOFException se o arquivo terminar no meio de um registro, o que
     *     indica truncamento e invalida a extração inteira
     */
    public <T> List<T> readAll(InputStream source, Function<FixedWidthRecord, T> mapper) throws IOException {
        List<T> records = new ArrayList<>();
        int width = layout.recordWidth();
        long lineNumber = 0;

        while (true) {
            byte[] buffer = new byte[width];
            int read = source.readNBytes(buffer, 0, width);
            if (read == 0) {
                return records;
            }
            lineNumber++;
            if (read < width) {
                throw new EOFException(
                    "Registro %d truncado: %d bytes lidos de %d esperados".formatted(lineNumber, read, width));
            }
            consumeSeparator(source, lineNumber);
            records.add(mapper.apply(new FixedWidthRecord(buffer, layout, lineNumber)));
        }
    }

    private void consumeSeparator(InputStream source, long lineNumber) throws IOException {
        int separator = source.read();
        if (separator == -1) {
            return;
        }
        // Um separador fora do lugar significa que os registros deixaram de
        // estar alinhados; seguir adiante produziria campos deslocados e
        // plausíveis, que é a falha mais perigosa de uma carga assim.
        if (separator != RECORD_SEPARATOR) {
            throw new IOException(
                "Separador ausente após o registro %d: encontrado 0x%02X".formatted(lineNumber, separator));
        }
    }
}
