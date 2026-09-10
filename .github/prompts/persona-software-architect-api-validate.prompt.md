---
name: "api-validate"
description: "Valide a implementação de uma API em relação ao contrato OpenAPI/AsyncAPI e informe cada divergência com o local explícito da correção."
argument-hint: "contract=<openapi.yaml|asyncapi.yaml> impl=<controllers path>"
agent: "software-architect"
tools: ["read", "search"]
---
# /api-validate

## Objetivo

Comparar a implementação com OpenAPI/AsyncAPI e relatar toda divergência como breaking, additive ou metadata, indicando correção no contrato ou no código. Verifique todas as operações e todos os endpoints.

## Quando usar

Após alterar um controlador ou manipulador e antes da integração.

## Pré-condições

- Contrato e implementação existem
- [`backend.instructions.md`](../instructions/backend.instructions.md) rege caminhos e status

## Entradas que a equipe deve fornecer

- Caminhos do contrato e da implementação e payloads de exemplo, se houver

## O que farei

- Compararei path, método, schemas, erros e autenticação nos dois sentidos
- Validarei exemplos e classificarei impacto e local da correção

## O que não farei

- Editar, inventar operações ou tratar campo opcional aditivo como breaking
- Decidir mudança irreversível; encaminharei a [`adr-draft`](../skills/adr-draft/SKILL.md)

## Formato da saída

Tabela `Endpoint | Tipo de divergência | Gravidade | Local da correção`, incluindo endpoints não documentados.

## Definição de pronto

- [ ] Cobertura de 100% do contrato e da implementação
- [ ] Breaking e additive separados; local da correção explícito

## Corpo do prompt

Você é `@software-architect`. Leia contrato e código. Para cada operação, compare path, HTTP, request, response, erros e autenticação. Procure endpoints não documentados. Valide exemplos. Classifique como breaking, additive ou metadata e indique contrato ou código. Não edite nem rebaixe a gravidade.

## Exemplo de chamada

```
/api-validate contract=backend/src/main/resources/openapi.yaml impl=backend/src/main/java/app/orders
```
