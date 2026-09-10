-- Caso de demonstração da dedução simplificada (REQ-016 a REQ-019).
--
-- Todos os beneficiários semeados até aqui produzem bruto entre 40,00 e
-- 138,84, abaixo do limite de 500,00 de CALCBENF.CALC-DISC. Nenhum deles
-- exercita a dedução no fluxo mensal, então a alíquota de 3% nunca foi
-- observada de ponta a ponta.
--
-- Os registros abaixo produzem bruto acima do limite com fatores neutros,
-- para que o valor seja conferível à mão:
--   1000,00 x 1,0000 (região 15) x 1,00 (sem dependentes)
--          x 1,0000 (renda ate 300,00) x 1,15 (66 anos) x 1,0000 (sem reajuste)
--   = 1150,00 bruto -> 34,50 de dedução -> 1115,50 líquido

-- Programa assistencial com faixa etária, teto de renda e código de
-- elegibilidade inertes, isolando a dedução como única regra sob observação.
INSERT INTO social_program (
    id, code, type, base_individual_amount, adjustment_factor, status,
    eligibility_code, age_min, age_max, max_income
) VALUES (
    '00000000-0000-0000-0000-000000000104',
    'A001',
    'A',
    1000.00,
    0.0000,
    'A',
    '     ',
    0,
    0,
    0.00
) ON CONFLICT (code) DO NOTHING;

-- Renda de 300,00 mantém o fator de renda em 1,0000 e, por ser menor que o
-- limite de 600,00 do tipo 'A', não aciona a recusa por renda sem dependentes.
INSERT INTO beneficiary (
    id, cpf, full_name, birth_date, status, program_code,
    family_income, dependent_count, region_code, nis, docs_ok
) VALUES (
    '00000000-0000-0000-0000-000000000005',
    '12345678909',
    'Pessoa Beneficiaria Bruto Alto',
    19600315,
    'A',
    'A001',
    300.00,
    0,
    '15',
    0,
    'S'
) ON CONFLICT (cpf) DO NOTHING;
