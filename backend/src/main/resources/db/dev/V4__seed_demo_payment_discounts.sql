-- Dados de demonstração para o recálculo de descontos.
--
-- Cria um pagamento já gerado com descontos registrados, permitindo exercitar
-- POST /api/v1/payments/{paymentId}/discount-calculations sem depender de uma
-- geração mensal prévia.
--
-- A sequência demonstra o teto de 30%: contribuição social de 5% (50,00),
-- judicial fixo (200,00) e sindical de 1% (10,00) somam 260,00; o
-- administrativo de 5% elevaria a 310,00 e o total é limitado a 300,00.
INSERT INTO beneficiary (
    id, cpf, full_name, birth_date, status, program_code,
    family_income, dependent_count, region_code
) VALUES (
    '00000000-0000-0000-0000-000000000002',
    '11144477735',
    'Pessoa Beneficiaria Descontos',
    19800101,
    'A',
    'P002',
    100.00,
    0,
    '15'
) ON CONFLICT (cpf) DO NOTHING;

INSERT INTO social_program (
    id, code, type, base_individual_amount, adjustment_factor, status
) VALUES (
    '00000000-0000-0000-0000-000000000102',
    'P002',
    'P',
    1000.00,
    0.0000,
    'A'
) ON CONFLICT (code) DO NOTHING;

INSERT INTO payment (
    id, cpf, program_code, reference_period,
    gross_amount, discount_amount, net_amount,
    generation_date, status, payment_type, bonus_amount
) VALUES (
    '00000000-0000-0000-0000-000000000201',
    '11144477735',
    'P002',
    202608,
    1000.00,
    0.00,
    1000.00,
    DATE '2026-08-31',
    'G',
    'N',
    0.00
) ON CONFLICT (cpf, reference_period) DO NOTHING;

INSERT INTO payment_discount (
    id, payment_id, sequence_number, type,
    fixed_amount, percentage, start_date, end_date, case_number
) VALUES
    ('00000000-0000-0000-0000-000000000301',
     '00000000-0000-0000-0000-000000000201', 1, 'J',
     200.00, 0.00, 0, 0, 'PROC-2026-000123'),
    ('00000000-0000-0000-0000-000000000302',
     '00000000-0000-0000-0000-000000000201', 2, 'S',
     0.00, 0.00, 0, 0, NULL),
    ('00000000-0000-0000-0000-000000000303',
     '00000000-0000-0000-0000-000000000201', 3, 'A',
     0.00, 5.00, 0, 0, NULL)
ON CONFLICT (payment_id, sequence_number) DO NOTHING;
