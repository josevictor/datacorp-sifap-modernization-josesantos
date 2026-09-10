-- Colunas de validação de elegibilidade (REQ-020 a REQ-033), espelhando
-- VALELEG.NSN. Os valores padrão desativam cada regra para que os dados
-- existentes preservem o comportamento anterior a esta feature: no legado,
-- zero significa "sem limite" em faixa etária e teto de renda, e o código de
-- elegibilidade em branco dispensa as exigências de NIS e dependentes.

ALTER TABLE beneficiary
    ADD COLUMN nis BIGINT NOT NULL DEFAULT 0,
    -- 'S' preserva o comportamento atual: sem esta coluna, a geração mensal
    -- nunca recusou por documentação. Iniciar com 'N' tornaria inelegível
    -- todo beneficiário de programa tipo 'A' já cadastrado.
    ADD COLUMN docs_ok VARCHAR(1) NOT NULL DEFAULT 'S';

ALTER TABLE social_program
    ADD COLUMN eligibility_code VARCHAR(5) NOT NULL DEFAULT '',
    ADD COLUMN age_min SMALLINT NOT NULL DEFAULT 0,
    ADD COLUMN age_max SMALLINT NOT NULL DEFAULT 0,
    ADD COLUMN max_income NUMERIC(7, 2) NOT NULL DEFAULT 0.00;
