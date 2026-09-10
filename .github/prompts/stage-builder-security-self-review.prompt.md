---
name: "security-self-review"
description: "Lista de autoavaliação de segurança e de problemas do OWASP Top 10 em uma funcionalidade recém-construída."
argument-hint: "context=<context> files=<Controller>.java,<Service>.java,<Entity>.java"
agent: "builder"
tools: ["read", "search", "edit"]
---
# /security-self-review

## Objetivo

Examinar uma funcionalidade segundo o OWASP Top 10 e produzir relatório priorizado. Não corrigir automaticamente; a equipe decide.

## Quando usar

Após implementar entidades, serviços, controladores e testes, antes da Etapa 4.

## Pré-condições

- O código existe e compila
- A equipe indica as classes

## Entradas que a equipe deve fornecer

- Controladores, serviços e entidades
- Nome do contexto delimitado

## O que farei

- Procurarei segredos, injeção SQL, autorização, validação, dados sensíveis em logs ou erros e ausência de rate limit
- Indicarei áreas que exigem scanner real

## O que não farei

- Executar scanner, corrigir automaticamente, inventar gravidade ou garantir completude

## Formato da saída

```markdown
# Autoavaliação de segurança — [Contexto delimitado]
## Resumo
Constatações: N no total | High: N | Medium: N | Low: N
## Constatações
| nº | Gravidade | Categoria | Arquivo:linha | Descrição | Remediação |
## Áreas que exigem varredura externa
## Aprovação
```

Grave em `03-implementation/security-review-[context].md`.

## Definição de pronto

- [ ] Autenticação de todos os endpoints, injeção em todas as consultas e validação de entradas foram verificadas
- [ ] Segredos estão ausentes ou sinalizados
- [ ] Gravidades estão justificadas
- [ ] Há área para varredura externa

## Corpo do prompt

Você é `@builder` e faz uma autoavaliação rápida, não uma auditoria formal.

**Etapa 1 — Segredos.** Procure “password”, “secret”, “key”, “token”, “api_key”, tokens Base64, valores literais em vez de `${ENV_VAR}` e `.env` versionado. Informe arquivo, linha, padrão com redação e gravidade High.

**Etapa 2 — Injeção SQL.** Procure concatenação, interpolação em `@Query`, `nativeQuery = true` para revisão e `JdbcTemplate` concatenado. Recomende parâmetros nomeados ou consultas derivadas.

**Etapa 3 — Autorização.** Em cada endpoint, verifique `@PreAuthorize`, `@Secured`, segurança por método e filtros. Endpoint público sem justificativa é High se escreve e Medium se apenas lê.

**Etapa 4 — Validação.** Verifique `@Valid`, Bean Validation e restrições `@Size` ou `@Pattern` em strings.

**Etapa 5 — Exposição.** Procure logs de senhas, tokens ou dados pessoais, stack traces e DTOs com `password`, `token` ou `ssn`.

**Etapa 6 — Rate limit.** Sinalize POST, PUT e DELETE sem limitação e registre como preocupação de produção.

**Etapa 7 — Relatório.** Ordene por gravidade e inclua áreas para SAST/DAST. O relatório é informativo; a equipe decide o que corrigir ou adiar.

## Exemplo de chamada

```
/security-self-review context=<context> files=<Controller>.java,<Service>.java,<Entity>.java
```
