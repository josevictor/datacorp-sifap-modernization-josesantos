---
name: "java-springboot"
description: "Aplique boas práticas de Spring Boot ao backend do SIFAP 2.0, delegando a lista detalhada à skill java-springboot."
argument-hint: "target=<file-or-module>"
agent: "implementer"
tools: ["read", "search", "edit"]
---
# /java-springboot

## Objetivo

Orientar a construção ou a revisão de uma fatia Spring Boot do backend do SIFAP 2.0: organização por funcionalidade, injeção por construtor, DTOs, tratamento global de exceções, transações na camada de serviço e fatias de teste. Assim, o código corresponde à stack fixa do kit. A lista detalhada está na skill [`java-springboot`](../skills/java-springboot/SKILL.md). Este prompt a aplica sem repeti-la.

> [!IMPORTANT]
> A stack é fixa: Java 21 + Spring Boot 3.3 + JPA/Hibernate + PostgreSQL 16. Não ofereça outro framework ou banco de dados como alternativa.

## Quando usar

Durante as Etapas 3 ou 4, ao construir ou revisar um módulo de backend, depois que seu contexto delimitado for conhecido.

## Pré-condições

- O módulo `backend/` foi criado; consulte `/create-spring-boot-java-project`
- O contexto delimitado e seu pacote foram identificados; consulte [`modular-monolith.instructions.md`](../instructions/modular-monolith.instructions.md)
- Os REQ-IDs implementados pelo módulo são conhecidos

## Entradas que a equipe deve fornecer

- `target`: o arquivo ou módulo a construir ou revisar
- O contexto delimitado correspondente e os REQ-IDs atendidos
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Seguirei as boas práticas da skill [`java-springboot`](../skills/java-springboot/SKILL.md) e as aplicarei ao destino
- Exigirei injeção por construtor, campos `private final`, limites por DTO e records de requisição com `@Valid`
- Manterei `@Transactional` na camada de serviço e encaminharei o acesso a dados pelo Spring Data JPA
- Direcionarei segredos a variáveis de ambiente respaldadas por Azure Key Vault e Managed Identity

## O que não farei

- Substituir por Quarkus, Micronaut, MongoDB, Redis ou qualquer componente alheio ao kit
- Recomendar HashiCorp Vault ou AWS Secrets Manager; o kit usa Azure Key Vault
- Expor entidades JPA diretamente por um controlador ou retornar `null` de um método público
- Colocar `@Transactional` em um repositório ou fixar um segredo no código

## Formato da saída

O código construído ou revisado, acompanhado de uma breve nota de conformidade:

```markdown
### Aplicado
- Injeção por construtor e `private final` em `PaymentService`
- Controlador `/api/v1/payments` com `@Valid PaymentRequest` e anotações OpenAPI
- `@Transactional` somente no método de serviço

### Sinalizado
- `PaymentController` retornava a entidade JPA → substituída por um DTO `PaymentResponse`
```

## Definição de pronto

- [ ] O código está organizado por funcionalidade, com injeção por construtor e campos imutáveis
- [ ] Os caminhos REST usam `/api/v1/{resource}` e cada endpoint tem anotações OpenAPI e `@Valid`
- [ ] `@Transactional` aparece somente na camada de serviço; nenhuma entidade é exposta
- [ ] Os segredos vêm do ambiente, pelo Azure Key Vault, e nunca estão fixados no código

## Corpo do prompt

A skill [`java-springboot`](../skills/java-springboot/SKILL.md) define as boas práticas em camadas. Leia-a e aplique-as ao destino.

**Etapa 1 — Posicionar o código.**
Confirme o pacote da funcionalidade e o contexto delimitado. Organize por domínio, não por camada.

**Etapa 2 — Aplicar a skill.**
Construa ou revise as camadas web, de serviço e de dados conforme a skill: DTOs no limite, tratamento de exceções com `@ControllerAdvice`, configuração tipada por `@ConfigurationProperties` e logs parametrizados com SLF4J.

**Etapa 3 — Respeitar as regras do kit.**
Mantenha Java 21 + Spring Boot 3.3 + PostgreSQL 16, obtenha segredos do Azure Key Vault e valide toda entrada com `@Valid`.

**Etapa 4 — Relatar.**
Liste as práticas aplicadas e as violações corrigidas.

## Exemplo de chamada

```
/java-springboot target=backend/src/main/java/com/sifap/payment
```
