<!-- markdownlint-disable MD024 -->

# ADR-NNNN: Título curto e decisivo

> **Trilha:** [Kit do Time](../../README.md) › [Documentação](../README.md) › [ADRs](README.md) › **Modelo**

> [!NOTE]
> Este é o modelo de ADR. Copie este arquivo para `NNNN-your-title.md`, substituindo `NNNN` pelo próximo número sequencial, como `0007`. Substitua cada bloco de instruções pelo conteúdo real da decisão.

| Campo | Valor |
|---|---|
| **Status** | proposed \| accepted \| deprecated \| superseded |
| **Data** | YYYY-MM-DD |
| **Autores** | Persona — Nome |
| **Substitui** | ADR-NNNN \| N/A |

---

## Contexto

> [!NOTE]
> Descreva o problema que motiva esta decisão. Faça referência ao objetivo de negócio, à restrição do legado ou à necessidade das partes interessadas. Seja específico. Cite REQ-IDs ou programas em `01-archaeology/legacy-sifap/` quando for relevante.

_Preencha esta seção._

---

## Decisão

> [!NOTE]
> Declare a mudança proposta na voz ativa. Use um ou dois parágrafos. Exemplos: "Adotaremos …", "Não migraremos …".

_Preencha esta seção._

---

## Alternativas consideradas

> [!NOTE]
> Liste pelo menos duas alternativas. Explique por que cada uma foi rejeitada.

| Alternativa | Por que foi rejeitada |
|---|---|
| Opção A | — |
| Opção B | — |

---

## Consequências

> [!NOTE]
> O que se torna mais fácil? O que se torna mais difícil? Há novos riscos?

- **Mais fácil:** —
- **Mais difícil:** —
- **Riscos:** —
- **Mitigações:** —

---

## Relacionados

- REQ-IDs: —
- ADRs: —
- Arquivos-fonte do legado: —

---

## Referências

> [!NOTE]
> Cite documentos, RFCs ou pesquisas que embasaram a decisão.

---

<details>
<summary><strong>Exemplo preenchido — ADR-0001: Adotar o Flyway para migrações de banco de dados</strong></summary>

| Campo | Valor |
|---|---|
| **Status** | accepted |
| **Data** | 2026-05-12 |
| **Autores** | DBA — Carla Souza |
| **Substitui** | N/A |

### Contexto

O SIFAP legado usa o Adabas, um banco de dados não relacional. A modernização adota o PostgreSQL 16. Precisamos de uma estratégia controlada de evolução do schema que rastreie mudanças, permita a recuperação após erros e se integre à CI. O programa `SIFAP-PAGTO.NSN` (linhas 45–78) revela que o ciclo mensal de pagamentos exige pelo menos três transformações do schema ao longo do tempo.

### Decisão

Adotaremos o Flyway como ferramenta de migração. Cada mudança no schema será representada por um arquivo `V<N>__description.sql` versionado no repositório. A CI executará `mvn flyway:migrate` em cada pull request para `develop`.

### Alternativas consideradas

| Alternativa | Por que foi rejeitada |
|---|---|
| Liquibase | Formato XML mais verboso e curva de aprendizado mais acentuada para o time durante esta imersão |
| Migrações manuais | Sem rastreabilidade, reversão automatizada ou integração com a CI |

### Consequências

- Mais fácil: rastreabilidade completa das mudanças no schema; a CI as valida antes da integração.
- Mais difícil: os arquivos de migração são imutáveis após a integração; cada correção exige um novo arquivo.
- Riscos: editar acidentalmente uma migração aplicada interrompe o Flyway.
- Mitigações: proteção da branch `develop` e a regra documentada em `troubleshooting.md`.

</details>

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [ADRs — Índice](README.md)<br/><sub>Índice das decisões registradas.</sub> | [Especificação moderna](../../02-modern-spec/GUIDE.md)<br/><sub>Onde os ADRs são produzidos.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
