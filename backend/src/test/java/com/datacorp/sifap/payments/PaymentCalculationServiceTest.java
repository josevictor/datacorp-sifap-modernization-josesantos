package com.datacorp.sifap.payments;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigDecimal;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class PaymentCalculationServiceTest {

    private final PaymentCalculationService service = new PaymentCalculationService();

    @Test
    void should_calculate_gross_amount_when_factors_are_known() {
        // REQ-005
        PaymentCalculation calculation = service.calculate(
            beneficiary("01", 19800101, 2, "01", "400.00"),
            program("P", "100.00", "0.1000"),
            YearMonthPeriod.of(202609));

        assertEquals(new BigDecimal("138.84"), calculation.grossAmount().value());
    }

    @Test
    void should_calculate_december_type_and_bonus_when_program_type_is_a() {
        // REQ-006, REQ-007
        PaymentCalculation calculation = service.calculate(
            beneficiary("15", 19800101, 0, "15", "100.00"),
            program("A", "100.00", "0.0000"),
            YearMonthPeriod.of(202612));

        assertAll(
            () -> assertEquals("D", calculation.paymentType()),
            () -> assertEquals(new BigDecimal("15.00"), calculation.bonusAmount().value()),
            () -> assertEquals(new BigDecimal("215.00"), calculation.grossAmount().value())
        );
    }

    @Test
    void should_calculate_normal_type_and_zero_bonus_when_period_is_not_december() {
        // REQ-006, REQ-007
        PaymentCalculation calculation = service.calculate(
            beneficiary("01", 19800101, 0, "15", "100.00"),
            program("A", "100.00", "0.0000"),
            YearMonthPeriod.of(202611));

        assertAll(
            () -> assertEquals("N", calculation.paymentType()),
            () -> assertEquals(new BigDecimal("0.00"), calculation.bonusAmount().value())
        );
    }

    @Test
    void should_truncate_amounts_when_fraction_has_more_than_two_decimal_places() {
        // REQ-005
        PaymentCalculation calculation = service.calculate(
            beneficiary("01", 19800101, 0, "01", "100.00"),
            program("P", "100.01", "0.0000"),
            YearMonthPeriod.of(202609));

        assertEquals(new BigDecimal("135.01"), calculation.grossAmount().value());
    }

    @Test
    void should_return_zero_net_amount_when_discount_exceeds_gross() {
        // REQ-008
        Money net = service.netAmount(new Money(new BigDecimal("10.00")), new Money(new BigDecimal("11.00")));

        assertEquals(new BigDecimal("0.00"), net.value());
    }

    @Test
    void should_keep_positive_net_amount_when_discount_is_lower_than_gross() {
        // REQ-008
        Money net = service.netAmount(new Money(new BigDecimal("10.00")), new Money(new BigDecimal("1.25")));

        assertEquals(new BigDecimal("8.75"), net.value());
    }

    @Test
    void should_apply_neutral_factor_when_region_is_outside_the_table() {
        // REQ-005 — espelha o ramo ELSE de BATCHPGT.NSP:390-394, que aplica
        // 1,0000 para região fora de 1 a 25. É o caminho da região 99.
        PaymentCalculation calculation = service.calculate(
            beneficiary("99", 19800101, 0, "P001", "100.00"),
            program("P", "100.00", "0.0000"),
            YearMonthPeriod.of(202609));

        assertEquals(new BigDecimal("100.00"), calculation.grossAmount().value());
    }

    @Test
    void should_apply_neutral_factor_when_region_is_not_numeric() {
        // REQ-005 — o DDM declara COD-REGION como alfanumérico A 2, então
        // nada impede um valor como 'NE' no cadastro. No legado isso é erro de
        // execução: o ON ERROR de BATCHPGT executa BACKOUT TRANSACTION e
        // TERMINATE 12, abortando a folha inteira por causa de um cadastro.
        // Aqui o pagamento degrada para o fator neutro em vez de derrubar o
        // processamento dos demais beneficiários.
        PaymentCalculation calculation = service.calculate(
            beneficiary("NE", 19800101, 0, "P001", "100.00"),
            program("P", "100.00", "0.0000"),
            YearMonthPeriod.of(202609));

        assertEquals(new BigDecimal("100.00"), calculation.grossAmount().value());
    }

    @Test
    void should_apply_neutral_factor_when_region_is_blank() {
        // REQ-005 — mesmo caso do anterior, com o valor em branco que o campo
        // alfanumérico também aceita.
        PaymentCalculation calculation = service.calculate(
            beneficiary("  ", 19800101, 0, "P001", "100.00"),
            program("P", "100.00", "0.0000"),
            YearMonthPeriod.of(202609));

        assertEquals(new BigDecimal("100.00"), calculation.grossAmount().value());
    }

    @Test
    void should_apply_table_factor_at_both_ends_of_the_valid_range() {
        // REQ-005 — limites inclusivos 1 e 25 do IF legado. A região 26 existe
        // na tabela de 27 posições do legado, mas é inalcançável pela própria
        // consulta; aqui ela recebe fator neutro.
        PaymentCalculation first = service.calculate(
            beneficiary("01", 19800101, 0, "P001", "100.00"),
            program("P", "100.00", "0.0000"),
            YearMonthPeriod.of(202609));
        PaymentCalculation last = service.calculate(
            beneficiary("25", 19800101, 0, "P001", "100.00"),
            program("P", "100.00", "0.0000"),
            YearMonthPeriod.of(202609));
        PaymentCalculation beyond = service.calculate(
            beneficiary("26", 19800101, 0, "P001", "100.00"),
            program("P", "100.00", "0.0000"),
            YearMonthPeriod.of(202609));

        assertAll(
            () -> assertEquals(new BigDecimal("135.00"), first.grossAmount().value()),
            () -> assertEquals(new BigDecimal("133.00"), last.grossAmount().value()),
            () -> assertEquals(new BigDecimal("100.00"), beyond.grossAmount().value())
        );
    }

    private Beneficiary beneficiary(String regionCode, int birthDate, int dependents, String programCode, String income) {
        return new Beneficiary(
            UUID.randomUUID(),
            "52998224725",
            "Pessoa Beneficiaria",
            birthDate,
            "A",
            programCode,
            new BigDecimal(income),
            dependents,
            regionCode);
    }

    private SocialProgram program(String type, String baseAmount, String adjustmentFactor) {
        return new SocialProgram(UUID.randomUUID(), "P001", type, new BigDecimal(baseAmount), new BigDecimal(adjustmentFactor), "A");
    }
}
