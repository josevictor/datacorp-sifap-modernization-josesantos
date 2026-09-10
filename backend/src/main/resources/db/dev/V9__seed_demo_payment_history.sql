-- Dados de demonstração da consulta de beneficiário (REQ-039 e REQ-040).
--
-- O beneficiário 39053344705, semeado em V6, recebe quinze pagamentos em
-- períodos deliberadamente fora de ordem de inserção. Assim, a consulta de
-- histórico só devolve os doze mais recentes se realmente ordenar por
-- período, e não pela ordem física dos registros.
--
-- É exatamente o caso que o legado erra: CONSBENF.NSP:270-284 rotula o bloco
-- como LAST 12 mas lê por NUM-CPF e corta no décimo segundo registro, sem
-- ordenar por período.

INSERT INTO payment (
    id, cpf, program_code, reference_period, gross_amount, discount_amount,
    net_amount, generation_date, status, payment_type, bonus_amount
)
SELECT
    ('00000000-0000-0000-0000-0000000009' || LPAD(ordem::text, 2, '0'))::uuid,
    '39053344705',
    'P003',
    periodo,
    800.00,
    0.00,
    800.00,
    DATE '2026-04-10',
    'G',
    'N',
    0.00
FROM (
    VALUES
        -- Inseridos fora de ordem cronológica de propósito.
        (1, 202512), (2, 202503), (3, 202601), (4, 202507), (5, 202510),
        (6, 202602), (7, 202501), (8, 202509), (9, 202603), (10, 202505),
        (11, 202511), (12, 202502), (13, 202508), (14, 202506), (15, 202504)
) AS historico(ordem, periodo)
ON CONFLICT (cpf, reference_period) DO NOTHING;
