-- Unicidade do NIS replicando a semântica do Adabas.
--
-- Na FDT do arquivo 150, `AM NUM-NIS` é declarado `DE,UQ,NU`. A combinação de
-- `UQ` (descritor único) com `NU` (supressão de nulos) não significa "único em
-- todos os registros": um campo suprimido não entra no índice, de modo que a
-- unicidade vale apenas entre os registros que têm NIS preenchido. Os 4,2
-- milhões de cadastros anteriores a 2001 — quando o campo foi criado — não
-- concorrem entre si.
--
-- O equivalente exato em PostgreSQL é um índice único parcial, não uma
-- constraint UNIQUE. Uma constraint comum trataria cada zero como um valor
-- disputado e rejeitaria o segundo cadastro sem NIS.
--
-- Isto sustenta no banco a guarda que BeneficiaryQueryService.findByNis já
-- aplica: o zero significa ausência de NIS e nunca é critério de busca.
CREATE UNIQUE INDEX ux_beneficiary_nis_present
    ON beneficiary (nis)
    WHERE nis > 0;
