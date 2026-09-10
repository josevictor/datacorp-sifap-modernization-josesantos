INSERT INTO beneficiary (
    id,
    cpf,
    full_name,
    birth_date,
    status,
    program_code,
    family_income,
    dependent_count,
    region_code
) VALUES (
    '00000000-0000-0000-0000-000000000001',
    '52998224725',
    'Pessoa Beneficiaria Demo',
    19800101,
    'A',
    'P001',
    400.00,
    2,
    '01'
) ON CONFLICT (cpf) DO NOTHING;

INSERT INTO social_program (
    id,
    code,
    type,
    base_individual_amount,
    adjustment_factor,
    status
) VALUES (
    '00000000-0000-0000-0000-000000000101',
    'P001',
    'A',
    100.00,
    0.1000,
    'A'
) ON CONFLICT (code) DO NOTHING;
