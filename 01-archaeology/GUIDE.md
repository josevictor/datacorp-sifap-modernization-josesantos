# Estágio 1 — Arqueologia Digital (90 min)

> **Trilha:** [Kit do Time](../README.md) › [Estágio 1](README.md) › **GUIDE**

**Cronograma de 90 minutos para ler os programas Natural atribuídos, registrar evidência rastreável e definir o escopo do protótipo.**

| Campo | Valor |
|---|---|
| **Público-alvo** | As 5 duplas |
| **Pré-requisitos** | Ler [`README.md`](README.md) e acessar o diretório `legacy-sifap/` |
| **Tempo estimado** | 90 min (11:00–12:00 + 13:30–14:00) |
| **Estágio** | Estágio 1 — Arqueologia |
| **Resultado esperado** | Catálogo de regras candidatas, relatório de descoberta e handoff H1 concluído |

> [!IMPORTANT]
> **Gate obrigatório.** Antes de escrever EARS no Estágio 2, a dupla precisa ter lido os programas Natural atribuídos e ter evidência para cada comportamento selecionado. Todo requisito formal seguinte precisa de um `source_legacy:` válido ou de `[GREENFIELD]` com justificativa. O gate não é uma meta de quantidade.

---

## Objetivo

Ler os programas Natural atribuídos, registrar evidência rastreável e escolher um escopo pequeno que possa virar uma feature. O objetivo não é explicar o SIFAP, o Sistema de Fiscalização e Administração de Pagamentos, por inteiro, produzir documentação enciclopédica nem resolver mistérios.

---

## Cronograma cronometrado

| Horário | Atividade | Resultado mínimo |
|---|---|---|
| 11:00–11:10 | Abrir os três programas atribuídos à dupla e combinar quem lê cada um. | Cobertura dos programas e nome de quem lê cada um. |
| 11:10–11:40 | Leitura guiada: entradas, saídas, chamadas e decisões de domínio. | Notas com caminhos e intervalos de linha. |
| 11:40–12:00 | Registrar regras candidatas e perguntas sem inferir comportamento ausente. | Evidência no catálogo e itens em aberto explícitos. |
| 13:30–13:45 | Consolidar apenas a evidência que sustenta o escopo do protótipo. | Catálogo e relatório de descoberta atualizados. |
| 13:45–13:55 | O PO prioriza **uma feature fina**; o time descarta ou adia o resto. | Decisão de escopo para o Estágio 2. |
| 13:55–14:00 | Handoff H1 com a Dupla 2. | Fontes, escopo e perguntas transferidos ao vivo. |

---

## Quem lê o quê

Cada dupla lê os três programas abaixo. A leitura pode focar nas decisões de domínio; não tente traduzir cada comando Natural nesta etapa.

| Dupla | Programas |
|---|---|
| 1 · Visão | `CADBENEF.NSP`, `CADDEPEN.NSP`, `CADPROG.NSP` |
| 2 · Arquitetura | `BATCHPGT.NSP`, `BATCHREL.NSP`, `BATCHCON.NSP` |
| 3 · Implementação | `CALCBENF.NSN`, `CALCCORR.NSP`, `CALCDSCT.NSP` |
| 4 · Qualidade | `VALBENEF.NSN`, `VALDOCS.NSP`, `VALELEG.NSN` |
| 5 · Operações | `CONSBENF.NSP`, `RELPGT.NSP`, `RELAUDIT.NSP` |

A Dupla 4 também revisa os DDMs necessários à feature selecionada. Mapear cada campo ou propor o schema completo não é obrigatório neste estágio.

---

## O que registrar

Use os [templates](templates/) como apoio. Para cada regra candidata dentro do escopo, registre pelo menos:

- uma descrição curta do comportamento observado;
- o caminho `.NSN` ou `.ddm` e, quando possível, o intervalo de linhas;
- a pergunta que ainda impede uma conclusão, sem transformá-la em requisito;
- o impacto da regra sobre a feature priorizada.

O `business-rules-catalog.md` é a entrada da spec formal; use o [template do catálogo](templates/business-rules-catalog.template.md) se o arquivo ainda não existir. O glossário, o mapa de dependências e o registro de mistérios podem ser enriquecidos se ajudarem o escopo, mas metas numéricas não bloqueiam o handoff.

> [!IMPORTANT]
> **Exceção — os mistérios têm denominador fixo.** O SIFAP contém **20 mistérios canônicos**, **4 por dupla**. Essa é a única meta numérica do Estágio 1, porque sem ela cada dupla reportava uma quantidade diferente depois de ler o mesmo material. Veja em [`mysteries-checklist.md`](mysteries-checklist.md) os IDs da sua dupla e registre-os em [`mysteries-found.md`](mysteries-found.md). Achados fora da lista são bônus e não mudam o denominador.

---

## Handoff H1

Em cinco minutos, a Dupla 1 entrega o seguinte à Dupla 2:

1. a feature fina selecionada e o que ficou fora de escopo;
2. as regras que podem virar requisitos, com os caminhos do legado;
3. as questões em aberto que **não podem** virar EARS;
4. referências de DDM e de dependências apenas quando afetarem a feature.

A Dupla 2 confirma que recebeu evidência suficiente para iniciar `specs/<NNN>-<feature>/spec.md`. Se não recebeu, o time reduz o escopo; não inventa uma fonte.

---

## Definição de pronto

- [ ] Os três programas atribuídos a cada dupla foram lidos.
- [ ] O comportamento selecionado tem evidência em `.NSN` ou `.ddm`, ou foi explicitamente separado como proposta greenfield.
- [ ] O catálogo identifica a origem de cada regra candidata.
- [ ] O relatório de descoberta registra o escopo e as perguntas relevantes.
- [ ] O handoff H1 aconteceu antes das 14:00.

---

## Referências

- [Checklist de exploração](LEGACY-EXPLORATION-CHECKLIST.md) — verificação do gate e critérios por dupla.
- [Guia do Estágio 2](../02-modern-spec/GUIDE.md) — próximo passo depois do handoff H1.
- [Como ler Natural](legacy-sifap/HOW-TO-READ-NATURAL.md) — tutorial de sintaxe para quem não é desenvolvedor.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Estágio 1 — README](README.md)<br/><sub>Visão geral do estágio.</sub> | [Checklist de Exploração](LEGACY-EXPLORATION-CHECKLIST.md)<br/><sub>Gate obrigatório antes do Estágio 2.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
