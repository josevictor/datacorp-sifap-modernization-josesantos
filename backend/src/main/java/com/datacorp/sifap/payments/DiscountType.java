package com.datacorp.sifap.payments;

import java.math.BigDecimal;

/**
 * Tipos de desconto registrados no grupo periódico do pagamento.
 *
 * <p>Cada tipo reproduz o ramo correspondente do {@code DECIDE ON FIRST VALUE}
 * de {@code CALCDSCT.NSP}.
 */
enum DiscountType {

    /** Judicial: valor fixo ou percentual. Isento do teto em seu próprio item. */
    COURT_ORDERED("J") {
        @Override
        Money amountFor(PaymentDiscount discount, Money gross) {
            return fixedOrPercentage(discount, gross);
        }
    },

    /** Pensão alimentícia: valor fixo ou percentual. */
    ALIMONY("P") {
        @Override
        Money amountFor(PaymentDiscount discount, Money gross) {
            return fixedOrPercentage(discount, gross);
        }
    },

    /** Imposto retido: somente percentual; valor fixo é ignorado. */
    WITHHOLDING_TAX("I") {
        @Override
        Money amountFor(PaymentDiscount discount, Money gross) {
            return percentage(discount, gross);
        }
    },

    /** Contribuição sindical: 1% fixo; valor e percentual registrados são ignorados. */
    UNION_DUES("S") {
        @Override
        Money amountFor(PaymentDiscount discount, Money gross) {
            return gross.multiply(new BigDecimal("0.01"));
        }
    },

    /** Administrativo: valor fixo ou percentual. */
    ADMINISTRATIVE("A") {
        @Override
        Money amountFor(PaymentDiscount discount, Money gross) {
            return fixedOrPercentage(discount, gross);
        }
    };

    private final String code;

    DiscountType(String code) {
        this.code = code;
    }

    abstract Money amountFor(PaymentDiscount discount, Money gross);

    String code() {
        return code;
    }

    boolean isExemptFromCap() {
        return this == COURT_ORDERED;
    }

    /**
     * Resolve o tipo pelo código legado.
     *
     * @return o tipo correspondente, ou {@code null} quando o código não é
     *     reconhecido. O legado trata esse caso com {@code NONE / IGNORE},
     *     descartando o desconto sem interromper o processamento (REQ-017).
     */
    static DiscountType fromCode(String code) {
        for (DiscountType type : values()) {
            if (type.code.equals(code)) {
                return type;
            }
        }
        return null;
    }

    private static Money fixedOrPercentage(PaymentDiscount discount, Money gross) {
        if (discount.fixedAmount().signum() > 0) {
            return new Money(discount.fixedAmount());
        }
        return percentage(discount, gross);
    }

    private static Money percentage(PaymentDiscount discount, Money gross) {
        return gross.multiply(discount.percentage().movePointLeft(2));
    }
}
