-- Trilha de acesso a dados pessoais (REQ-042), espelhando o bloco
-- PERSONAL DATA ACCESS TRAIL de CONSBENF.NSP:168-179, que cita a
-- IN-TCU 63/2010.
--
-- Campos legados deliberadamente ausentes:
--   USR-EVENT       - não há autenticação nesta feature; a trilha registra
--                     que houve acesso, não por quem
--   NAME-JOB-BATCH  - específico de execução batch
--   STAT-BATCH      - específico de execução batch
--
-- Preferimos omitir a coluna a criá-la sempre vazia: uma coluna nula em
-- toda linha dá falsa impressão de rastreabilidade de autoria.

CREATE TABLE audit_trail (
    id UUID PRIMARY KEY,
    action_code VARCHAR(2) NOT NULL,
    entity_type VARCHAR(4) NOT NULL,
    entity_id VARCHAR(11) NOT NULL,
    affected_cpf VARCHAR(11) NOT NULL,
    description VARCHAR(120) NOT NULL,
    module_code VARCHAR(10) NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX ix_audit_trail_affected_cpf
    ON audit_trail (affected_cpf, occurred_at);
