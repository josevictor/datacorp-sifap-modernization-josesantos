package com.datacorp.sifap.migration;

import java.math.BigDecimal;

/**
 * Registro de beneficiário lido da extração legada, ainda sem validação.
 *
 * <p>Contém apenas os campos do escopo de carga — os que o sistema moderno
 * efetivamente consome — e não os 69 campos do cadastro legado. Os valores são
 * transportados como foram lidos, para que a decisão de aceitar ou colocar em
 * quarentena pertença a quem valida, e não a quem lê.
 *
 * @param lineNumber posição do registro no arquivo, em base 1, usada nos
 *     relatórios de quarentena
 * @param registration {@code NUM-REGISTRATION}
 * @param cpf {@code NUM-CPF}, sem formatação
 * @param fullName {@code FULL-NAME}, já sem os espaços à direita
 * @param birthDate {@code DT-BIRTH} no formato {@code AAAAMMDD}
 * @param nis {@code NUM-NIS}; {@code 0} representa ausência, e não um NIS real
 * @param regionCode {@code COD-REGION}
 * @param programCode {@code COD-PROGRAM}
 * @param status {@code STAT-BENEFICIARY}
 * @param familyIncome {@code AMT-FAMILY-INCOME}, decodificado do compactado
 * @param dependentCount {@code QTY-DEPEND}
 * @param docsOk {@code IND-DOCS-OK}
 */
public record LegacyBeneficiaryRecord(
    long lineNumber,
    String registration,
    String cpf,
    String fullName,
    int birthDate,
    long nis,
    String regionCode,
    String programCode,
    String status,
    BigDecimal familyIncome,
    int dependentCount,
    String docsOk
) {
}
