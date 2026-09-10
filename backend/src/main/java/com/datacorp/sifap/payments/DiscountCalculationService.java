package com.datacorp.sifap.payments;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * Cálculo detalhado de descontos, traduzido de {@code CALCDSCT.NSP}.
 *
 * <p>Aplica a contribuição social obrigatória, percorre os descontos vigentes
 * e limita o total ao teto de 30% do valor bruto.
 */
@Service
class DiscountCalculationService {

    private static final BigDecimal CAP_RATE = new BigDecimal("0.30");

    /**
     * Apura o total de descontos de um pagamento (REQ-010 a REQ-019).
     *
     * @param referenceDate data corrente no formato {@code YYYYMMDD}, usada
     *     para avaliar a vigência de cada desconto
     */
    Money totalFor(Money gross, List<PaymentDiscount> discounts, int referenceDate) {
        Money total = SocialContributionTable.contributionFor(gross);
        Money cap = gross.multiply(CAP_RATE);

        for (PaymentDiscount discount : discounts) {
            if (!discount.isEffectiveOn(referenceDate)) {
                continue;
            }

            DiscountType type = DiscountType.fromCode(discount.type());
            if (type == null) {
                continue;
            }

            total = total.add(type.amountFor(discount, gross));

            // O legado avalia o teto dentro do laço, sobre o total acumulado,
            // sempre que o item corrente não é judicial. Como o total é
            // acumulado, um item não judicial pode reduzir valor originado de
            // um desconto judicial, embora o tipo J seja declarado isento.
            // O comportamento é preservado deliberadamente (REQ-018) e a
            // questão está registrada como achado BONUS em
            // 01-archaeology/mysteries-found.md.
            if (!type.isExemptFromCap() && total.isGreaterThan(cap)) {
                total = cap;
            }
        }

        return total;
    }
}
