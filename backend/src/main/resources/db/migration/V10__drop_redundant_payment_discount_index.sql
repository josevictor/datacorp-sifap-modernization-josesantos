-- Remove índice redundante em payment_discount.
--
-- A constraint `ux_payment_discount_sequence UNIQUE (payment_id,
-- sequence_number)` já cria implicitamente um índice B-tree sobre exatamente
-- as mesmas colunas, na mesma ordem. O índice `ix_payment_discount_payment`
-- criado logo abaixo dela em V3 é uma duplicata: nenhuma consulta pode
-- preferi-lo, e o PostgreSQL escolherá o da constraint.
--
-- O custo da duplicata não é o espaço, é a escrita: cada INSERT em
-- payment_discount mantinha duas estruturas idênticas.
--
-- V3 não é editada. Migração já aplicada não se altera; corrige-se adiante.

DROP INDEX IF EXISTS ix_payment_discount_payment;

-- NOTA DE INDEXAÇÃO sobre `ix_audit_trail_affected_cpf`, criado em V8.
--
-- Registrada aqui, e não em V8, porque aquela migração já foi aplicada e
-- alterá-la quebraria o checksum do Flyway.
--
-- Aquele índice antecipa a consulta "quem acessou o cadastro deste CPF, e
-- quando", que a IN-TCU 63/2010 torna inevitável. Hoje o código só o exercita
-- em teste, então é a única estrutura deste esquema criada por antecipação, e
-- não por padrão de consulta observado.
--
-- Se a consulta de auditoria não existir até a primeira revisão de
-- desempenho, remova-o: em tabela somente de acréscimo, índice não usado é
-- custo puro de escrita.
