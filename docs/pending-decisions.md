# Decisões pendentes de pessoas responsáveis

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Decisões pendentes**

**Registro das pendências que a equipe de implementação não pode fechar sozinha: cada uma exige decisão de negócio ou acesso a dados de produção.**

| Campo | Valor |
|---|---|
| **Público-alvo** | Líder Técnico, Coordenação de Benefícios, DBA e operação do batch |
| **Finalidade** | Substituir as issues do GitHub enquanto a CLI `gh` não está disponível no ambiente |
| **Última atualização** | 2026-09-10 |

> [!NOTE]
> Quando a CLI `gh` estiver disponível, promova cada item abaixo a uma issue e
> registre aqui o número correspondente. Este arquivo existe para que nenhuma
> pendência dependa de memória ou de conversa informal.

---

## Situação

| # | Pendência | Responsável | Bloqueia |
|---|---|---|---|
| 1 | Ratificar a separação entre a dedução simplificada e `CALCDSCT` | Coordenação de Benefícios | Fechamento de `SIFAP-M-09` e do ADR-0004 |
| 2 | Medir o impacto das regras por tipo de programa | Coordenação de Benefícios + DBA + operação do batch | Implantação da feature `003` |
| 3 | Alinhar com a Dupla 4 a autoria de `VALELEG` | Dupla 3 e Dupla 4 | Nada; evita retrabalho |

---

## 1. Ratificar a separação entre a dedução simplificada e `CALCDSCT`

O [ADR-0004](adr/0004-simplified-deduction-monthly-flow.md) está em `proposed` e
propõe a resolução de `SIFAP-M-09`.

**A parte técnica está fechada por evidência de código.** O job mensal
`SIFAPJ01` executa apenas `BATCHPGT` (`SIFAPJ01.jcl:70-77`), que aplica a
dedução simplificada inline e gera a remessa bancária
(`BATCHPGT.NSP:455-500`). `CALCDSCT` é interativo (`CALCDSCT.NSP:71-75`) e não
integra o fluxo mensal. A documentação de 2012 afirma o contrário e está
errada.

**O que falta é decisão de negócio, não análise.** A separação define qual
valor chega à pessoa beneficiária. Um recálculo por `CALCDSCT` posterior à
remessa diverge do valor já transmitido ao banco, sem mecanismo de conciliação
localizado no código.

---

## 2. Medir o impacto das regras por tipo de programa (T224)

**Bloqueia a implantação da feature `003`, não o merge.**

A migração `V5` nasce com padrões inertes que preservam o comportamento atual
para faixa etária, teto de renda e NIS: no legado, zero significa "sem limite".

As regras por tipo de programa **não têm esse escape**. São literais fixos em
`VALELEG.NSN:196-243`, sem parâmetro que as desative:

| Tipo | Recusa |
|---|---|
| `A` | Documentação incompleta; renda acima de `600,00` sem dependentes |
| `P` | Idade abaixo de 60 |
| `T` | Idade fora da faixa de 16 a 65 |
| outro | Sempre |

**Consequência:** um beneficiário ativo hoje em programa cujo tipo o recusa
deixa de receber na primeira execução com a validação ativa.

A consulta de medição está pronta em
[`impact-query.sql`](../specs/003-elegibilidade/impact-query.sql). É somente
leitura e vive fora de `db/migration` para que o Flyway não a execute. Deve
rodar contra uma cópia dos dados de produção, substituindo o ano do período a
processar.

**A consulta já foi verificada** contra o banco de desenvolvimento em
2026-09-10: detectou o único beneficiário violador entre os cinco semeados,
ignorou os conformes, respeitou o desvio da região `99` e restringiu-se a
cadastros ativos. Não é preciso auditá-la antes de usar; basta executá-la.

Como executar, ajustando conexão e ano do período:

```bash
psql -U <usuario> -d <base> -v ON_ERROR_STOP=1 \
  < specs/003-elegibilidade/impact-query.sql
```

| Resultado | Encaminhamento sugerido |
|---|---|
| Zero afetados | Implantar sem ação adicional |
| Poucos afetados | Tratar caso a caso antes da implantação |
| Muitos afetados | Não implantar; a regra legada provavelmente não reflete a operação real |

---

## 3. Alinhar com a Dupla 4 a autoria de `VALELEG`

`VALELEG.NSN` estava no escopo da Dupla 4 (`SIFAP-M-13` a `SIFAP-M-16`), mas
foi implementado pela Dupla 3 na feature `003`.

**Motivo:** `BATCHPGT.NSP:369-379` chama `VALELEG` por `CALLNAT` antes do
cálculo, e a feature `001` gerava pagamento sem validação alguma. Era uma
lacuna de fidelidade na própria feature da Dupla 3.

Os achados foram registrados como `BONUS` em
[`mysteries-found.md`](../01-archaeology/mysteries-found.md), sem reivindicar
os IDs canônicos da Dupla 4.

Arquivos tocados, para evitar conflito: `EligibilityValidationService`,
`EligibilityCode`, `EligibilityReason`, `EligibilityStatus`, `ProgramTypeRule`
e a migração `V5`.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Mistérios encontrados](../01-archaeology/mysteries-found.md)<br/><sub>Questões abertas do sistema legado.</sub> | [Decisões de escopo](../02-modern-spec/scope-decisions.md)<br/><sub>O que entrou e o que ficou de fora.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
