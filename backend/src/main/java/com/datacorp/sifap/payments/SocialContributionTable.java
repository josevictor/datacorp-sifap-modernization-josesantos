package com.datacorp.sifap.payments;

import java.math.BigDecimal;

/**
 * Faixas e alíquotas da contribuição social obrigatória.
 *
 * <p>Espelha as tabelas {@code #BAND-CONTRIB} e {@code #RATE-CONTRIB} de
 * {@code CALCDSCT.NSP}. A alíquota aplicada é a da primeira faixa cujo limite
 * seja maior ou igual ao valor bruto.
 *
 * <p>Valores brutos acima do último limite não casam nenhuma faixa e produzem
 * contribuição zero. Isso reproduz o laço legado, que encerra sem aplicar
 * alíquota quando nenhuma condição é satisfeita.
 */
final class SocialContributionTable {

    private record Band(BigDecimal limit, BigDecimal rate) {
    }

    private static final Band[] BANDS = {
        new Band(new BigDecimal("500.00"), new BigDecimal("0.03")),
        new Band(new BigDecimal("1000.00"), new BigDecimal("0.05")),
        new Band(new BigDecimal("2000.00"), new BigDecimal("0.07")),
        new Band(new BigDecimal("9999.99"), new BigDecimal("0.09"))
    };

    private SocialContributionTable() {
    }

    static Money contributionFor(Money gross) {
        for (Band band : BANDS) {
            if (gross.value().compareTo(band.limit()) <= 0) {
                return gross.multiply(band.rate());
            }
        }
        return Money.zero();
    }
}
