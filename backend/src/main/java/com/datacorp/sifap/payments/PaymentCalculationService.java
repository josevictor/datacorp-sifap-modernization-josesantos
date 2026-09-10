package com.datacorp.sifap.payments;

import java.math.BigDecimal;
import org.springframework.stereotype.Service;

@Service
class PaymentCalculationService {

    private static final BigDecimal[] REGION_FACTORS = {
        new BigDecimal("1.3500"), new BigDecimal("1.3200"), new BigDecimal("1.3000"),
        new BigDecimal("1.2800"), new BigDecimal("1.3100"), new BigDecimal("1.4000"),
        new BigDecimal("1.3800"), new BigDecimal("1.3500"), new BigDecimal("1.3200"),
        new BigDecimal("1.3600"), new BigDecimal("1.1000"), new BigDecimal("1.1200"),
        new BigDecimal("1.0800"), new BigDecimal("1.0500"), new BigDecimal("1.0000"),
        new BigDecimal("1.0500"), new BigDecimal("1.0700"), new BigDecimal("1.0300"),
        new BigDecimal("1.1500"), new BigDecimal("1.2000"), new BigDecimal("1.1800"),
        new BigDecimal("1.2500"), new BigDecimal("1.1000"), new BigDecimal("1.2200"),
        new BigDecimal("1.3300")
    };

    PaymentCalculation calculate(Beneficiary beneficiary, SocialProgram program, YearMonthPeriod period) {
        Money benefit = new Money(program.baseIndividualAmount()
            .multiply(regionFactor(beneficiary.regionCode()))
            .multiply(familyFactor(beneficiary.dependentCount()))
            .multiply(incomeFactor(beneficiary.familyIncome()))
            .multiply(ageFactor(period.year() - beneficiary.birthYear()))
            .multiply(BigDecimal.ONE.add(program.adjustmentFactor())));

        Money gross = benefit;
        Money bonus = Money.zero();
        String paymentType = "N";

        if (period.month() == 12) {
            paymentType = "D";
            Money thirteenth = new Money(program.baseIndividualAmount()
                .multiply(regionFactor(beneficiary.regionCode()))
                .multiply(ageFactor(period.year() - beneficiary.birthYear())));
            gross = gross.add(thirteenth);
            if ("A".equals(program.type())) {
                bonus = benefit.multiply(new BigDecimal("0.15"));
                gross = gross.add(bonus);
            }
        }

        Money discount = simplifiedDiscount(gross);
        Money net = netAmount(gross, discount);

        return new PaymentCalculation(gross, discount, bonus, net, paymentType);
    }

    Money netAmount(Money gross, Money discount) {
        Money net = gross.subtract(discount);
        if (net.isNegative()) {
            return Money.zero();
        }
        return net;
    }

    private BigDecimal regionFactor(String regionCode) {
        try {
            int region = Integer.parseInt(regionCode);
            if (region >= 1 && region <= REGION_FACTORS.length) {
                return REGION_FACTORS[region - 1];
            }
        } catch (NumberFormatException ex) {
            return BigDecimal.ONE;
        }
        return BigDecimal.ONE;
    }

    private BigDecimal familyFactor(int dependentCount) {
        if (dependentCount == 0) {
            return BigDecimal.ONE;
        }
        if (dependentCount <= 2) {
            return BigDecimal.ONE.add(new BigDecimal(dependentCount).multiply(new BigDecimal("0.0500")));
        }
        if (dependentCount <= 4) {
            return new BigDecimal("1.1000")
                .add(new BigDecimal(dependentCount - 2).multiply(new BigDecimal("0.0300")));
        }
        return new BigDecimal("1.1600")
            .add(new BigDecimal(dependentCount - 4).multiply(new BigDecimal("0.0200")));
    }

    private BigDecimal incomeFactor(BigDecimal income) {
        if (income.compareTo(new BigDecimal("300.00")) <= 0) {
            return new BigDecimal("1.0000");
        }
        if (income.compareTo(new BigDecimal("600.00")) <= 0) {
            return new BigDecimal("0.8500");
        }
        if (income.compareTo(new BigDecimal("1000.00")) <= 0) {
            return new BigDecimal("0.7000");
        }
        if (income.compareTo(new BigDecimal("1500.00")) <= 0) {
            return new BigDecimal("0.5500");
        }
        return new BigDecimal("0.4000");
    }

    private BigDecimal ageFactor(int age) {
        if (age >= 65) {
            return new BigDecimal("1.1500");
        }
        if (age >= 60) {
            return new BigDecimal("1.1000");
        }
        if (age < 18) {
            return new BigDecimal("1.0500");
        }
        return BigDecimal.ONE;
    }

    private Money simplifiedDiscount(Money gross) {
        Money threshold = new Money(new BigDecimal("500.00"));
        if (gross.isGreaterThan(threshold)) {
            return gross.multiply(new BigDecimal("0.03"));
        }
        return Money.zero();
    }
}
