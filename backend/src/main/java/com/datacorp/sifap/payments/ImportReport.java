package com.datacorp.sifap.payments;

import java.util.List;

/**
 * Resultado de uma carga de dados legados.
 *
 * <p>Vale a identidade de reconciliação
 * {@code read == loaded + skipped + rejected.size()}: todo registro lido tem um
 * destino explícito. {@link #isReconciled()} verifica essa identidade, e é ela
 * que distingue uma carga completa de uma carga que perdeu registros pelo
 * caminho.
 *
 * @param <R> enumeração dos motivos de recusa da carga
 * @param read registros lidos do arquivo
 * @param loaded registros gravados nesta execução
 * @param skipped registros já presentes na base, ignorados por idempotência
 * @param rejected registros recusados, com o respectivo motivo
 */
public record ImportReport<R extends Enum<R>>(
    int read,
    int loaded,
    int skipped,
    List<RejectedRecord<R>> rejected
) {

    public ImportReport {
        rejected = List.copyOf(rejected);
    }

    /**
     * @return {@code true} se todo registro lido foi carregado, ignorado ou recusado
     */
    public boolean isReconciled() {
        return read == loaded + skipped + rejected.size();
    }

    /**
     * Registro recusado e sua causa.
     *
     * @param <R> enumeração dos motivos de recusa
     * @param lineNumber posição no arquivo, em base 1
     * @param reference identificador do registro na origem — matrícula ou número
     *     do pagamento —, nunca o CPF, que não pode aparecer em log
     * @param reason motivo da recusa
     */
    public record RejectedRecord<R extends Enum<R>>(long lineNumber, String reference, R reason) {
    }
}
