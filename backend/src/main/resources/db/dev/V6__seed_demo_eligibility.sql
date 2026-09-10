-- Dados de demonstração da validação de elegibilidade (REQ-020 a REQ-033).
--
-- O beneficiário 'P002' semeado em V4 já serve como caso inelegível: o
-- programa é do tipo 'P', que exige 60 anos, e o cadastro tem data de
-- nascimento de 1980. Uma geração mensal para ele é ignorada com o motivo
-- PENSION_AGE_BELOW_MINIMUM.
--
-- Os registros abaixo completam os demais casos observáveis.

-- Programa previdenciário com faixa etária e teto de renda preenchidos,
-- demonstrando as regras que os dados existentes mantêm desativadas por
-- padrão.
INSERT INTO social_program (
    id, code, type, base_individual_amount, adjustment_factor, status,
    eligibility_code, age_min, age_max, max_income
) VALUES (
    '00000000-0000-0000-0000-000000000103',
    'P003',
    'P',
    100.00,
    0.0000,
    'A',
    'RD   ',
    60,
    0,
    2000.00
) ON CONFLICT (code) DO NOTHING;

-- Elegível: 66 anos, NIS cadastrado, um dependente e renda abaixo do teto.
INSERT INTO beneficiary (
    id, cpf, full_name, birth_date, status, program_code,
    family_income, dependent_count, region_code, nis, docs_ok
) VALUES (
    '00000000-0000-0000-0000-000000000003',
    '39053344705',
    'Pessoa Beneficiaria Elegivel',
    19600315,
    'A',
    'P003',
    800.00,
    1,
    '15',
    12345678901,
    'S'
) ON CONFLICT (cpf) DO NOTHING;

-- Região 99: viola faixa etária, teto de renda, NIS e dependentes, mas o
-- desvio de VALELEG.NSN:120-128 o declara elegível assim mesmo.
-- Comportamento preservado por fidelidade; questão aberta SIFAP-M-12.
INSERT INTO beneficiary (
    id, cpf, full_name, birth_date, status, program_code,
    family_income, dependent_count, region_code, nis, docs_ok
) VALUES (
    '00000000-0000-0000-0000-000000000004',
    '15350946056',
    'Pessoa Beneficiaria Regiao Especial',
    20000101,
    'A',
    'P003',
    9000.00,
    0,
    '99',
    0,
    'N'
) ON CONFLICT (cpf) DO NOTHING;
