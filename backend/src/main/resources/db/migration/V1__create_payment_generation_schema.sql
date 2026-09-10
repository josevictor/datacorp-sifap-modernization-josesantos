CREATE TABLE beneficiary (
    id UUID PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL,
    full_name VARCHAR(60) NOT NULL,
    birth_date INTEGER NOT NULL,
    status VARCHAR(1) NOT NULL,
    program_code VARCHAR(4) NOT NULL,
    family_income NUMERIC(9, 2) NOT NULL,
    dependent_count INTEGER NOT NULL,
    region_code VARCHAR(2) NOT NULL,
    CONSTRAINT ux_beneficiary_cpf UNIQUE (cpf)
);

CREATE TABLE social_program (
    id UUID PRIMARY KEY,
    code VARCHAR(4) NOT NULL,
    type VARCHAR(1) NOT NULL,
    base_individual_amount NUMERIC(7, 2) NOT NULL,
    adjustment_factor NUMERIC(5, 4) NOT NULL,
    status VARCHAR(1) NOT NULL,
    CONSTRAINT ux_social_program_code UNIQUE (code)
);

CREATE TABLE payment (
    id UUID PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL,
    program_code VARCHAR(4) NOT NULL,
    reference_period INTEGER NOT NULL,
    gross_amount NUMERIC(9, 2) NOT NULL,
    discount_amount NUMERIC(7, 2) NOT NULL,
    net_amount NUMERIC(9, 2) NOT NULL,
    generation_date DATE NOT NULL,
    status VARCHAR(1) NOT NULL,
    payment_type VARCHAR(1) NOT NULL,
    bonus_amount NUMERIC(9, 2) NOT NULL,
    CONSTRAINT ux_payment_cpf_period UNIQUE (cpf, reference_period)
);

CREATE INDEX ix_payment_program_period_status
    ON payment (program_code, reference_period, status);

CREATE TABLE payment_rejection (
    id UUID PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL,
    reference_period INTEGER NOT NULL,
    reason VARCHAR(40) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX ix_payment_rejection_period
    ON payment_rejection (reference_period);
