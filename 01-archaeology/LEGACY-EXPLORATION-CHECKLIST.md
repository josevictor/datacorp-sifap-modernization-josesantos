# Checklist de Exploração do Legado

> **Trilha:** [Kit do Time](../README.md) › [Estágio 1](README.md) › **Checklist de Exploração**

**Gate obrigatório antes do Estágio 2.** Este checklist garante que cada dupla leu os programas atribuídos e que as regras candidatas são rastreáveis até o código legado.

| Campo | Valor |
|---|---|
| **Público-alvo** | Todas as duplas — preencher durante o Estágio 1 |
| **Pré-requisitos** | Acesso a `legacy-sifap/natural-programs/` e `adabas-ddms/` |
| **Tempo estimado** | Preenchido ao longo dos 90 minutos |
| **Estágio** | Estágio 1 — Arqueologia |
| **Resultado esperado** | Matriz de leitura completa por dupla e critérios de conclusão verificados |

> [!IMPORTANT]
> **Gate obrigatório antes do Estágio 2.** Nenhum requisito EARS é aceito sem referência a um programa Natural ou arquivo DDM. Requisitos greenfield (sem equivalente no legado) precisam ser marcados com `[GREENFIELD]` e justificados por escrito na spec.

> [!WARNING]
> Na edição anterior da imersão, vários times pularam a exploração do legado e escreveram specs baseadas apenas no briefing de modernização. O resultado foram especificações que não preservavam as regras de negócio reais dos 29 anos do SIFAP como Sistema de Fiscalização e Administração de Pagamentos. Este gate é obrigatório.

---

## 1. A regra de rastreabilidade

Todo `REQ-ID` em `specs/<NNN>-<feature>/spec.md` precisa ter uma linha `source_legacy:` apontando para uma destas opções:

- um membro Natural, como `.NSP` ou `.NSN`, em `01-archaeology/legacy-sifap/natural-programs/` (de preferência com intervalo de linhas);
- um arquivo `.ddm` específico em `01-archaeology/legacy-sifap/adabas-ddms/`;
- `[GREENFIELD]` com uma justificativa de uma linha.

O CI rejeita PRs para `develop` se algum `REQ-ID` estiver sem a linha `source_legacy:`. Os facilitadores fazem verificações por amostragem durante o handoff H2, às 15:00.

---

## 2. Os 15 programas Natural — quem lê o quê

Cada dupla recebe 3 programas. Nenhum programa pode ficar sem leitor.

| Dupla | Programas a ler | Mistérios | Por quê |
|---|---|---|---|
| **1 · Visão** (PO + RE) | `CADBENEF.NSP`, `CADDEPEN.NSP`, `CADPROG.NSP` | `SIFAP-M-01` … `M-04` | Lógica de cadastro — entidades centrais que viram sujeitos EARS. |
| **2 · Arquitetura** (EA + SA) | `BATCHPGT.NSP`, `BATCHREL.NSP`, `BATCHCON.NSP` | `SIFAP-M-05` … `M-08` | Fluxos batch revelam fronteiras de módulo (bounded contexts). |
| **3 · Implementação** (TL + Dev) | `CALCBENF.NSN`, `CALCCORR.NSP`, `CALCDSCT.NSP`\* | `SIFAP-M-09` … `M-12` | Os cálculos são onde o código moderno vai viver; o time precisa reproduzi-los. |
| **4 · Qualidade** (DBA + QA) | `VALBENEF.NSN`, `VALDOCS.NSP`, `VALELEG.NSN` | `SIFAP-M-13` … `M-16` | Validações viram testes; o DBA também mapeia os campos dos DDMs. |
| **5 · Operações** (DevOps + TW) | `CONSBENF.NSP`, `RELPGT.NSP`, `RELAUDIT.NSP` | `SIFAP-M-17` … `M-20` | Caminhos de leitura alimentam o glossário e o runbook. |

\* `CALCDSCT.NSP` é **leitura de apoio** para a Dupla 3: nenhum mistério canônico mora nele. Ainda assim vale perguntar por que ele existe e quem o chama.

> [!IMPORTANT]
> **São 20 mistérios canônicos, 4 por dupla** — essa é a única meta numérica do Estágio 1. Os IDs e as áreas estão em [`mysteries-checklist.md`](mysteries-checklist.md); registre-os em [`mysteries-found.md`](mysteries-found.md). Achados fora da lista contam como bônus e **não** mudam o denominador.

### Checklist para cada programa

Para cada programa atribuído à sua dupla, registre notas de leitura suficientes para confirmar que ele foi examinado:

- [ ] **Identifique o programa.** Registre nome, autor e ano da última modificação.
- [ ] **Mapeie as entradas.** Quais DDMs ele lê.
- [ ] **Mapeie as saídas.** Quais DDMs ele escreve.
- [ ] **Registre as chamadas.** Outros programas chamados por `CALLNAT`.
- [ ] **Catalogue as regras candidatas.** Quando o programa contiver uma regra relevante ao escopo, registre-a em `business-rules-catalog.md` com `Programa de origem` e intervalo de linhas.

> [!WARNING]
> Uma linha sem `Programa de origem` não sustenta um requisito EARS.

---

## 3. Os 4 DDMs — mapeamento de campos

A Dupla 4 (DBA + QA) lidera. Todas as outras duplas contribuem com revisões.

| DDM | Responsável | Artefato-alvo no PostgreSQL |
|---|---|---|
| `BENEFIC.ddm` | Dupla 4 | <!-- definir a partir da evidência --> |
| `PAYMENT.ddm` | Dupla 4 | <!-- definir a partir da evidência --> |
| `SOCPROG.ddm` | Dupla 4 | <!-- definir a partir da evidência --> |
| `AUDIT.ddm` | Dupla 4 | <!-- definir a partir da evidência --> |

Revise os DDMs necessários à feature selecionada. O mapeamento completo para PostgreSQL pertence ao planejamento e à implementação; não é pré-requisito para começar a spec.

---

## 4. Registro de questões em aberto

Use [`mysteries-checklist.md`](mysteries-checklist.md) para registrar questões em aberto sem antecipar respostas. O registro é um catálogo de incertezas, não um gabarito nem uma fonte de regras.

Registre em `mysteries-found.md` apenas as questões que afetam o escopo. Cada registro precisa conter:

| Campo | Descrição |
|---|---|
| Questão em aberto | Texto da pergunta, sem conclusão |
| Evidência | `path:line` |
| Impacto | Efeito sobre o escopo |
| Hipótese | Explicitamente marcada como não confirmada |
| Responsável | Pessoa ou área que pode validar |
| Status | `aberta` / `aguardando validação humana` / `fechada após validação humana` |

Uma questão só pode ser fechada ou usada como base para uma regra depois de validação humana explícita, apoiada na evidência registrada.

---

## 5. Verificação antes de abrir o Estágio 2

Por volta das 13:50, um facilitador confere o trabalho da dupla contra esta matriz. Uma linha vermelha bloqueia a passagem para o Estágio 2.

| Verificação | Critério do gate |
|---|---|
| Leitura atribuída | Cada dupla confirmou a leitura dos três programas que recebeu. |
| Catálogo de regras | Toda regra candidata dentro do escopo tem `Programa de origem` preenchido. |
| Escopo | O relatório de descoberta identifica uma feature pequena e o que foi adiado. |
| Questões em aberto | As incertezas relevantes foram registradas sem virar requisitos. |

---

## 6. Formato obrigatório do Estágio 2

Escreva EARS apenas em `specs/<NNN>-<feature>/spec.md`, usando o Spec-Kit. Todo `REQ-ID` precisa de um padrão EARS, critérios Given/When/Then e `source_legacy:`. Não conclua nenhum requisito até o time confirmar a fonte ou a justificativa greenfield.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [GUIDE do Estágio 1](GUIDE.md)<br/><sub>Cronograma cronometrado.</sub> | [Templates](templates/)<br/><sub>Modelos preenchíveis para os artefatos do estágio.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
