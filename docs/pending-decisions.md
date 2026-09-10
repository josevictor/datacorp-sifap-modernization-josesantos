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
| 2 | Medir o impacto das regras por tipo de programa | Coordenação de Benefícios + DBA + operação do batch | Implantação da feature `003` — **medição no laboratório indica 30,3% de recusa** |
| 3 | Alinhar com a Dupla 4 a autoria de `VALELEG` | Dupla 3 e Dupla 4 | Nada; evita retrabalho |
| 4 | Atualizar o Next.js para uma versão sem CVE | Líder Técnico | Nada hoje; bloqueia qualquer exposição pública do frontend |
| 5 | Decidir a conversão de `docs_ok` em branco nos cadastros anteriores a 2012 | Coordenação de Benefícios | Carga da base legada |
| 6 | Decidir a origem de `dependent_count` nos cadastros anteriores a 2013 | Coordenação de Benefícios | Carga da base legada |
| 7 | Decidir se `NUM-REGISTRATION` é preservado como chave de reconciliação | Arquitetura + DBA | Carga da base legada |

---

## 1. Ratificar a separação entre a dedução simplificada e `CALCDSCT`

O [ADR-0004](adr/0004-simplified-deduction-monthly-flow.md) está em `proposed` e
propõe a resolução de `SIFAP-M-09`.

**A questão técnica está encerrada.** `BATCHPGT` contém exatamente três
`CALLNAT` — `SUBVALCP`, `VALELEG` e `CALCBENF` — e nenhuma chamada a
`CALCDSCT`. A cadeia de quatro elos foi projetada e documentada no PDA em 2011
pelo próprio autor do `CALCDSCT`, mas apenas dois foram ligados: o programa usa
`INPUT` de tela e é incompatível com `CALLNAT`.

Em outras palavras, a dedução simplificada **não é o desvio de uma integração
que existiu**. É a única dedução que já rodou no fluxo mensal desde 1997.

As três fontes que afirmam o contrário — o PDA, o cabeçalho do batch e a
documentação de 2012 — descrevem a arquitetura pretendida. A de 2012 declara no
próprio texto que não teve acesso ao programa e erra outros três pontos
verificáveis no mesmo trecho.

**O que falta é uma confirmação de negócio, não análise.** A Coordenação de
Benefícios precisa dizer se sabe que o valor pago usa a regra simplificada e se
considera isso correto. A evidência mostra o que o sistema faz e por quê; não
mostra se é o desejado.

Fica registrado, como item próprio, que um recálculo por `CALCDSCT` posterior à
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

> [!WARNING]
> A equipe da imersão **não tem acesso a dados de produção**. A medição abaixo
> foi feita sobre a extração sintética do laboratório e **não substitui** a
> execução contra o cadastro real.

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

### Medição no laboratório (2026-09-10)

As mesmas regras aplicadas aos 500 cadastros de
[`legacy-seed-data/`](../01-archaeology/legacy-seed-data/), com ano de
referência 2018:

| Resultado | Valor |
|---|---:|
| Beneficiários ativos avaliados | 475 |
| Protegidos pelo desvio da região `99` | 5 |
| **Afetados — deixariam de receber** | **144 (30,3%)** |
| ├ Documentação incompleta | 106 |
| └ Renda acima de 600,00 sem dependentes | 38 |

**Os dois números têm pesos de evidência muito diferentes.**

Os 106 por documentação são **artefato do gerador**, não sinal do mundo real:
`IND-DOCS-OK` é sorteado como `N` em 25% dos casos, e o número simplesmente
reflete esse sorteio. Não diz nada sobre a distribuição em produção.

Os 38 por renda sem dependentes são **estruturais**. Decorrem do cruzamento de
faixas de renda com contagem de dependentes que o gerador constrói
deliberadamente para cobrir as bandas de cálculo. Esse mecanismo existe em
produção, ainda que a proporção seja desconhecida.

O caso `78933359478` ilustra o problema melhor que o agregado:
`MARIA MARTINS OLIVEIRA`, 71 anos, ativa, com quatro pagamentos registrados,
renda familiar de `1.000,00` em família de quatro pessoas e nenhum dependente
cadastrado. **Recebe no legado e seria recusada pela regra.** Sua renda per
capita é `250,00`, bem abaixo do teto de `600,00` do próprio programa: a regra
de tipo `A` usa renda **familiar**, não per capita.

**O que a medição autoriza concluir:** a regra recusa uma fração não trivial de
beneficiários ativos, e o mecanismo de recusa por renda sem dependentes atinge
justamente quem o programa parece destinado a atender. **O que não autoriza:**
estimar o percentual em produção. Os 30,3% são do laboratório.

| Resultado | Encaminhamento sugerido |
|---|---|
| Zero afetados | Implantar sem ação adicional |
| Poucos afetados | Tratar caso a caso antes da implantação |
| Muitos afetados | Não implantar; a regra legada provavelmente não reflete a operação real |

A medição no laboratório cai na terceira faixa. Ela não decide a implantação,
mas eleva a prioridade da medição real e sugere que a pergunta a levar à
Coordenação de Benefícios não é apenas "quantos são", e sim **se a regra de
renda familiar sem dependentes reflete a intenção do programa**.

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

## 4. Atualizar o Next.js para uma versão sem CVE

O módulo `frontend/` foi criado com `next@15.1.6`, que o registro do npm marca
com vulnerabilidade de segurança
([CVE-2025-66478](https://nextjs.org/blog/CVE-2025-66478)). A instalação também
reporta oito vulnerabilidades no conjunto de dependências, duas delas críticas.

**Decisão registrada em 2026-09-10:** a atualização foi adiada
deliberadamente para não interromper a entrega da feature `004`. O risco atual
é baixo porque o frontend roda apenas em `localhost`, por Docker, sem exposição
de rede e sem dados reais.

**O risco deixa de ser baixo no momento em que qualquer uma destas coisas
acontecer:** o frontend ser publicado em ambiente acessível, receber dados de
produção ou entrar em pipeline de implantação. Nenhuma delas deve ocorrer antes
da atualização.

Encaminhamento: fixar a versão corrigida mais recente da linha 15.x e reexecutar
a suíte do frontend. É uma troca de versão, sem mudança de código esperada.

---

## 5. Conversão de `docs_ok` em branco nos cadastros anteriores a 2012

`CL IND-DOCS-OK` foi criado em 2012 e é `FI` (armazenamento fixo), então os
cadastros anteriores carregam **branco** — um terceiro estado que o domínio
`S`/`N` não prevê. A coluna moderna é `NOT NULL DEFAULT 'S'`.

| Conversão | Consequência |
|---|---|
| branco → `'S'` | Concede elegibilidade documental a quem nunca foi verificado |
| branco → `'N'` | Bloqueia cadastros válidos anteriores a 2012 |

**Não existe escolha tecnicamente correta.** As duas alteram o resultado da
validação de elegibilidade para uma população que o legado nunca classificou.
A decisão é de negócio e deve virar ADR antes da carga.

> [!WARNING]
> A extração do laboratório **não exercita este caso**: o gerador preenche
> `IND-DOCS-OK` sempre com `S` ou `N`, nunca em branco. Uma carga bem sucedida
> nos 500 registros sintéticos não demonstra que a decisão foi tomada — apenas
> que a população que a exige não está presente.

---

## 6. Origem de `dependent_count` nos cadastros anteriores a 2013

`CK QTY-DEPEND` foi criado em 2013. Cadastros anteriores têm o campo vazio, que
a carga leria como zero, enquanto os dependentes reais permanecem no grupo
periódico `DA GRP-DEPEND` (1:10) — fora do escopo A.

Como `dependent_count` alimenta a elegibilidade, o efeito é concreto:
beneficiários com dependentes reais entrariam com zero e poderiam ser recusados
indevidamente.

**Recomendação técnica:** derivar o valor da contagem de ocorrências ativas de
`GRP-DEPEND` durante a carga. Não exige tabela nova nem amplia o escopo do
esquema — basta ler o grupo periódico na origem. A alternativa é aceitar o erro
conscientemente, e isso precisa ser dito por escrito.

> [!WARNING]
> A extração do laboratório **não exercita este caso**: o gerador mantém
> `QTY-DEPEND` sempre coerente com o grupo periódico. A população anterior a
> 2013, que produz a divergência, não está nos dados sintéticos.

---

## 7. Preservação de `NUM-REGISTRATION` como chave de reconciliação

`AA NUM-REGISTRATION` não é campo de negócio e não está no escopo A. Ainda
assim, sem ele não há como reconciliar um registro carregado com sua origem,
reexecutar uma faixa com segurança nem fazer carga incremental.

O projeto de carga já o mantém na tabela de staging. A pergunta é se ele deve
sobreviver como coluna de auditoria em `beneficiary`. Sem isso, qualquer
divergência apurada depois da carga só pode ser investigada por CPF, que é dado
pessoal e nem sempre suficiente.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Mistérios encontrados](../01-archaeology/mysteries-found.md)<br/><sub>Questões abertas do sistema legado.</sub> | [Decisões de escopo](../02-modern-spec/scope-decisions.md)<br/><sub>O que entrou e o que ficou de fora.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
