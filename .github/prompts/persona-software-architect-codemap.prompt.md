---
name: "codemap"
description: "Produza um mapa de código navegável, no nível de serviço, para um módulo do SIFAP 2.0: componentes, dependências diretas, cobertura de REQ-ID, linhagem legada e pontos de integração."
argument-hint: "service=<name> path=<root created by the team> spec=specs/<NNN>-<feature>/spec.md"
agent: "software-architect"
tools: ["read", "search", "edit"]
---
# /codemap

## Objetivo

Produzir `docs/codemap-<service>.md` para localizar componentes, dependências diretas, REQ-IDs e linhagem em dez minutos.

## Quando usar

Após a equipe criar um serviço e sempre que sua estrutura mudar.

## Pré-condições

- Serviço e `spec.md` existem
- [`modular-monolith.instructions.md`](../instructions/modular-monolith.instructions.md) rege dependências

## Entradas que a equipe deve fornecer

- Serviço, raiz, especificação, inclusão de testes e mapa anterior

## O que farei

- Agruparei Java por `controller`, `service`, `domain`, `repository`, `infrastructure`, `config`; TypeScript por `app/`, `components/`, `lib/`, `server/`
- Registrarei função confirmada, dependências diretas, `@implements REQ-NNN`, estado, API, testes e linhagem confirmada
- Gerarei Mermaid e tabela pesquisável; sinalizarei direção errada, mais de cinco saídas e código sem entradas

## O que não farei

- Gerar automaticamente por imports, listar transitivas ou inventar REQ-IDs, endpoints, responsabilidades ou fatos Natural
- Decidir contextos; use `/impl-plan` ou [`adr-draft`](../skills/adr-draft/SKILL.md)

## Formato da saída

Documento com diagrama, tabela `Tipo | FQN | Função | REQ-IDs | Entrada | Saída`, API, estado, linhagem e problemas observados.

## Definição de pronto

- [ ] Mermaid reflete componentes reais; tabela cobre o serviço
- [ ] REQ-IDs ausentes são explícitos; dependências são diretas
- [ ] Linhagem tem evidência e o documento está ligado a `docs/CODEMAP.md`

## Corpo do prompt

Você é `@software-architect`. Confirme escopo e mapa anterior. Liste componentes por camada e função comprovada. Mapeie chamadas diretas e contratos estáveis. Localize `@implements REQ-NNN` sem inventar lacunas. Registre somente a origem Natural confirmada; use “não mapeado” no restante. Sinalize violações de camada, god classes e código sem entrada. Grave Mermaid e tabelas e vincule a `docs/CODEMAP.md`.

## Exemplo de chamada

```
/codemap service=registration path=backend/src/main/java/app/registration spec=specs/014-registration/spec.md
```
