# ADR-XXX: Título da decisão

> **Trilha:** [Kit do Time](../README.md) › [Estágio 2](README.md) › **Template de ADR**

> [!NOTE]
> Este arquivo é um template de apoio. Copie-o para `ADR-NNN-title.md` e preencha a cópia. Não edite o original.
> Use este template quando uma decisão de arquitetura bloquear o `plan.md` da feature.

![Estágio 2](https://img.shields.io/badge/Est%C3%A1gio-2%20%C2%B7%20Especifica%C3%A7%C3%A3o-171717?style=flat-square) ![Tipo: template de ADR](https://img.shields.io/badge/Tipo-Modelo%20de%20ADR-737373?style=flat-square)

| Campo | Valor |
|---|---|
| **Data** | `YYYY-MM-DD` |
| **Status** | Proposta / Aceita / Rejeitada / Substituída pela ADR-YYY |
| **Responsáveis pela decisão** | Nomes das pessoas do time envolvidas |
| **Feature relacionada** | `specs/<NNN>-<feature>/` |

---

## Conceito: ADR (Architecture Decision Record)

Uma ADR é o registro formal de uma decisão de arquitetura relevante. Ela documenta o contexto que levou à decisão, as alternativas avaliadas, a opção escolhida e as consequências esperadas.

**Por que isso importa:** decisões técnicas tomadas verbalmente durante a imersão se perdem. Uma ADR de duas páginas permite que qualquer pessoa revisora do PR entenda por que o sistema foi projetado de determinada maneira, sem consultar quem tomou a decisão às 14:30 de um dia intenso.

**Regra de ouro:** sempre liste o "caminho não escolhido". Sem ele, a ADR se torna uma descrição da implementação, não um registro de decisão.

**Quando criar uma:** somente quando a decisão bloquear o `plan.md`. Se a decisão couber em um comentário de commit, ela não precisa de uma ADR.

---

## Contexto

> Descreva o problema ou a necessidade que motivou esta decisão.
> Inclua restrições, requisitos e informações relevantes.
> Seja específico: "precisamos de um banco de dados" não é suficiente.

<!-- preencher -->

---

## Opções consideradas

### Opção 1: <!-- nome -->

| Aspecto | Avaliação |
|---|---|
| **Descrição** | Como funcionaria |
| **Vantagens** | Liste-as |
| **Desvantagens** | Liste-as |

### Opção 2: <!-- nome -->

| Aspecto | Avaliação |
|---|---|
| **Descrição** | Como funcionaria |
| **Vantagens** | Liste-as |
| **Desvantagens** | Liste-as |

### Opção 3: <!-- nome, opcional -->

| Aspecto | Avaliação |
|---|---|
| **Descrição** | Como funcionaria |
| **Vantagens** | Liste-as |
| **Desvantagens** | Liste-as |

---

## Decisão

**Decidimos** <!-- ação ou escolha selecionada -->.

---

## Justificativa

> Explique por que esta opção foi escolhida em vez das outras.
> Relacione-a aos requisitos, às restrições e ao contexto.

<!-- preencher -->

---

## Consequências

### Positivas

- <!-- consequência positiva 1 -->

### Negativas

- <!-- consequência negativa 1 e como mitigá-la -->

### Riscos

- <!-- risco identificado e plano de contingência -->

---

## Referências

- <!-- link ou documento relevante -->
- Requisito EARS relacionado: `REQ-XXX`

<details>
<summary><strong>Exemplo preenchido — ADR-001: banco de dados do SIFAP 2.0</strong></summary>

| Campo | Valor |
|---|---|
| **Data** | 2026-05-10 |
| **Status** | Aceita |
| **Responsáveis pela decisão** | Dupla 2 (Enterprise Architect + Software Architect) |
| **Feature relacionada** | `specs/001-pagamento-beneficio/` |

**Contexto:** o SIFAP legado (Sistema de Fiscalização e Administração de Pagamentos) usa o Adabas, um banco de dados navegacional. A modernização precisa de um banco de dados relacional compatível com JPA/Hibernate e com suporte do time de operações.

**Opções:**

- PostgreSQL 16: código aberto, suporte a JSONB e Testcontainers disponível.
- MySQL 8: amplo suporte, mas menor adoção em ambientes governamentais brasileiros.

**Decisão:** PostgreSQL 16.

**Justificativa:** adoção consolidada em sistemas do setor público, suporte nativo a tipos avançados (JSONB para campos variáveis dos DDMs) e integração com Testcontainers sem licença adicional.

**Consequências positivas:** o Testcontainers simplifica os testes de integração. **Consequências negativas:** o time de DBA precisa conhecer PostgreSQL.

</details>

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [GUIDE do Estágio 2](GUIDE.md)<br/><sub>Instruções passo a passo do estágio.</sub> | [GUIDE do Estágio 2](GUIDE.md)<br/><sub>Conduza a decisão com o time.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
