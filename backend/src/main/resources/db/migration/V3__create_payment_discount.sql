-- Descontos do pagamento.
--
-- Equivale ao grupo periódico GRP-DISC do DDM PAYMENT, que no Adabas admitia
-- até 8 ocorrências dentro do próprio registro de pagamento. O limite de 8 era
-- restrição do formato, não regra de negócio observada, e por isso não é
-- reproduzido como constraint.
--
-- As datas permanecem no formato numérico YYYYMMDD do legado porque REQ-012
-- depende de end_date = 0 significar "sem término".
CREATE TABLE payment_discount (
    id UUID PRIMARY KEY,
    payment_id UUID NOT NULL,
    -- Ordem de aplicação. REQ-018 reproduz o teto do legado aplicado ao total
    -- acumulado dentro do laço, então a ordem altera o resultado e precisa ser
    -- determinística.
    sequence_number INTEGER NOT NULL,
    type VARCHAR(1) NOT NULL,
    fixed_amount NUMERIC(9, 2) NOT NULL DEFAULT 0,
    percentage NUMERIC(5, 2) NOT NULL DEFAULT 0,
    start_date INTEGER NOT NULL DEFAULT 0,
    end_date INTEGER NOT NULL DEFAULT 0,
    case_number VARCHAR(20),
    CONSTRAINT fk_payment_discount_payment
        FOREIGN KEY (payment_id) REFERENCES payment (id) ON DELETE CASCADE,
    CONSTRAINT ux_payment_discount_sequence
        UNIQUE (payment_id, sequence_number),
    CONSTRAINT ck_payment_discount_amounts
        CHECK (fixed_amount >= 0 AND percentage >= 0)
);

CREATE INDEX ix_payment_discount_payment
    ON payment_discount (payment_id, sequence_number);
