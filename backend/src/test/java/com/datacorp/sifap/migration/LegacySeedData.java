package com.datacorp.sifap.migration;

import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Localiza a extração legada usada pelos testes de carga.
 *
 * <p>Os arquivos ficam em {@code 01-archaeology/legacy-seed-data/}, fora do
 * módulo {@code backend/}, e por isso o caminho depende de onde a suíte é
 * executada: na IDE o diretório de trabalho é {@code backend/}, enquanto no
 * contêiner de testes a pasta é montada em outro ponto. A variável de ambiente
 * {@code SIFAP_LEGACY_SEED_DIR} resolve essa diferença, e o valor padrão atende
 * à execução local.
 */
public final class LegacySeedData {

    private static final String LOCATION_VARIABLE = "SIFAP_LEGACY_SEED_DIR";
    private static final String DEFAULT_LOCATION = "../01-archaeology/legacy-seed-data";

    private LegacySeedData() {
    }

    /**
     * @return diretório da extração legada
     * @throws IllegalStateException se o diretório não existir, para que a causa
     *     apareça como configuração ausente e não como arquivo não encontrado
     */
    public static Path directory() {
        String configured = System.getenv(LOCATION_VARIABLE);
        Path directory = Path.of(configured == null ? DEFAULT_LOCATION : configured);
        if (!Files.isDirectory(directory)) {
            throw new IllegalStateException(
                "Extração legada não encontrada em \"%s\". Defina %s para o diretório de legacy-seed-data."
                    .formatted(directory.toAbsolutePath(), LOCATION_VARIABLE));
        }
        return directory;
    }

    /**
     * @param fileName nome do arquivo dentro da extração
     * @return caminho do arquivo solicitado
     */
    public static Path file(String fileName) {
        return directory().resolve(fileName);
    }
}
