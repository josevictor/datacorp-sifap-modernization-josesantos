-- Medição de impacto da validação de elegibilidade (T224).
--
-- NÃO é uma migração. Este arquivo vive fora de db/migration de propósito:
-- é somente leitura e deve ser executado sob demanda contra uma cópia dos
-- dados de produção, nunca aplicado pelo Flyway.
--
-- Motivo da medição
-- -----------------
-- A migração V5 nasce com padrões inertes: idade zero, teto de renda zero e
-- código de elegibilidade em branco desativam suas regras, exatamente como no
-- legado. Esses casos são seguros.
--
-- As regras por tipo de programa NÃO têm esse escape. Em VALELEG.NSN:196-243
-- os limites são literais fixos no código, sem parâmetro que os desative:
--
--   tipo 'A' recusa documentação incompleta e recusa renda acima de 600,00
--            quando não há dependentes
--   tipo 'P' recusa idade abaixo de 60
--   tipo 'T' recusa idade fora da faixa de 16 a 65
--   outro    recusa sempre
--
-- Um beneficiário ativo hoje em programa cujo tipo o recusa deixa de receber
-- na primeira execução com a validação ativa. Esta consulta mede quantos são,
-- antes da implantação.
--
-- Substitua 2026 pelo ano do período que será processado: a idade usa o ano
-- do período, conforme a fonte única definida no plano da feature 003.
--
-- Verificação
-- -----------
-- Executada em 2026-09-10 contra o banco de desenvolvimento, com os cinco
-- beneficiários semeados por V2, V4, V6 e V7. Retornou exatamente uma linha,
-- IDADE_ABAIXO_DO_MINIMO_PREVIDENCIARIO / P002 / P / 1, conforme previsto:
-- detectou o violador, ignorou os conformes, respeitou o desvio da região 99
-- e restringiu-se a cadastros ativos.

WITH parametros AS (
    SELECT 2026 AS ano_periodo
),
avaliado AS (
    SELECT
        b.cpf,
        b.region_code,
        p.code AS program_code,
        p.type AS program_type,
        b.family_income,
        b.dependent_count,
        b.docs_ok,
        (SELECT ano_periodo FROM parametros) - (b.birth_date / 10000) AS idade
    FROM beneficiary b
    JOIN social_program p ON p.code = b.program_code
    -- O batch já filtra o beneficiário inativo antes de chamar VALELEG, então
    -- só quem está ativo pode ser afetado por esta mudança.
    WHERE b.status = 'A'
      AND p.status = 'A'
),
classificado AS (
    SELECT
        a.*,
        CASE
            -- Região 99 dispensa todas as validações (VALELEG.NSN:120-128).
            -- Questão aberta SIFAP-M-12: enquanto o desvio existir, esses
            -- beneficiários não são afetados pela mudança.
            WHEN a.region_code = '99' THEN NULL
            WHEN a.program_type = 'A' AND a.docs_ok <> 'S'
                THEN 'DOCUMENTACAO_INCOMPLETA'
            WHEN a.program_type = 'A' AND a.family_income > 600.00 AND a.dependent_count < 1
                THEN 'RENDA_SEM_DEPENDENTES'
            WHEN a.program_type = 'P' AND a.idade < 60
                THEN 'IDADE_ABAIXO_DO_MINIMO_PREVIDENCIARIO'
            WHEN a.program_type = 'T' AND (a.idade < 16 OR a.idade > 65)
                THEN 'IDADE_FORA_DA_FAIXA_DE_TRABALHO'
            WHEN a.program_type NOT IN ('A', 'P', 'T')
                THEN 'TIPO_DE_PROGRAMA_DESCONHECIDO'
        END AS motivo_de_recusa
    FROM avaliado a
)

-- Resumo por motivo e programa: o número que decide a implantação.
SELECT
    motivo_de_recusa,
    program_code,
    program_type,
    COUNT(*) AS beneficiarios_afetados
FROM classificado
WHERE motivo_de_recusa IS NOT NULL
GROUP BY motivo_de_recusa, program_code, program_type
ORDER BY beneficiarios_afetados DESC;

-- Contagem de quem escapa apenas pela região 99. Se o desvio for removido
-- quando SIFAP-M-12 for decidido, este grupo passa a ser avaliado também.
-- Consulta independente, para rodar separadamente:
--
-- SELECT COUNT(*)
-- FROM beneficiary b
-- JOIN social_program p ON p.code = b.program_code
-- WHERE b.status = 'A' AND p.status = 'A' AND b.region_code = '99';
