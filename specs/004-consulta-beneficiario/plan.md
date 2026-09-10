# Plano técnico — Consulta de beneficiário

Feature `004-consulta-beneficiario`, cobrindo `REQ-034` a `REQ-042`.

---

## Recorte

Esta é a primeira feature com interface. Ela adiciona dois componentes ao
sistema:

| Camada | Entrega |
|---|---|
| Backend | `GET /api/v1/beneficiaries` com busca por CPF ou NIS, cadastro mascarado, histórico de doze pagamentos e trilha de auditoria |
| Frontend | Módulo `frontend/` em Next.js 15 com uma página de consulta |

---

## Backend

### Busca por dois critérios

O legado decide o critério por um campo de tela `#TYPE-SEARCH`
(`CONSBENF.NSP:146-166`). No sistema moderno, o critério vem do parâmetro de
consulta usado: `?cpf=` ou `?nis=`. Exatamente um deles é obrigatório; informar
ambos ou nenhum é erro de solicitação.

A validação de CPF reaproveita `CpfValidator`, já usado pela feature `001`. O
NIS não é validado antes da busca, porque o legado também não valida: a chamada
a `SUBVALCP` está apenas no ramo de CPF.

### Máscara de CPF: divergência deliberada

`MASK-CPF` tem dois ramos (`CONSBENF.NSP:292-311`):

| Condição | Saída legada | Dígitos expostos |
|---|---|---|
| CPF com 11 dígitos | `***.***.247-25` | Cinco últimos |
| CPF com menos de 11 | `529.***.***-**` | **Três primeiros** |

O sistema moderno implementa **apenas o primeiro ramo**. O segundo é uma falha
de privacidade: as duas máscaras protegem partes diferentes do documento, então
quem visse ambas as telas reconstruiria a maior parte do CPF.

Esta é a primeira divergência do projeto motivada por **política de dados
pessoais**, e não por regra de negócio. As instruções do repositório proíbem
expor CPF, e replicar o ramo inseguro violaria essa regra em nome de uma
fidelidade que o próprio código legado marca como defeito
(`KNOWN INCONSISTENCY`).

O ramo não é alcançável na base moderna: a coluna `cpf` é `VARCHAR(11)` e a
validação exige onze dígitos. Preservá-lo seria replicar código morto inseguro.

Achado registrado em `mysteries-found.md`; a aprovação de auditoria que o
comentário legado exige continua pendente para o sistema legado.

### Ordenação do histórico: correção deliberada

O legado rotula o bloco como `PAYMENT HISTORY (LAST 12)` mas executa
`READ PAYMENT-V BY NUM-CPF`, que percorre pelo descritor de CPF e corta na
décima segunda ocorrência (`CONSBENF.NSP:270-284`). Não há ordenação por
período nem leitura descendente.

Com mais de doze pagamentos, os exibidos podem ser os **mais antigos**, sob um
rótulo que promete os mais recentes.

`REQ-040` corrige isso e é o único requisito `[GREENFIELD]` da feature. A
correção é segura porque o legado não define comportamento para o caso: o
rótulo e o código discordam entre si, então não há contrato a preservar.

### Trilha de auditoria

`CONSBENF` grava um registro por consulta bem-sucedida, com ação `CO` e
entidade `BENF` (`CONSBENF.NSP:168-179`), citando a IN-TCU 63/2010.

A migração `V8` cria `audit_trail` com o subconjunto de colunas que o sistema
moderno consegue preencher. Campos legados sem equivalente ficam de fora, em
vez de nascerem vazios:

| Campo legado | Situação no sistema moderno |
|---|---|
| `COD-ACTION`, `TYPE-ENTITY`, `ID-ENTITY` | Preenchidos |
| `NUM-CPF-AFFECTED` | Preenchido |
| `DESCR-ACTION`, `COD-MODULE` | Preenchidos |
| `USR-EVENT` | **Fora** — não há autenticação nesta feature |
| `NAME-JOB-BATCH`, `STAT-BATCH` | **Fora** — específicos de execução batch |

`USR-EVENT` é a ausência mais relevante: a trilha registra que houve acesso, mas
não por quem. Enquanto não houver autenticação, a trilha é parcial, e isso fica
registrado em `tasks.md` como limitação conhecida, não como campo esquecido.

### Formato da resposta

O CPF sai **somente mascarado**. O identificador do beneficiário na resposta é
o `id`, não o CPF, para que a interface não precise trafegar o documento
completo.

O histórico não repete o CPF em cada item.

---

## Frontend

### Estrutura

O módulo `frontend/` nasce nesta feature. A stack é a definida nas instruções
do repositório: Next.js 15 App Router, TypeScript strict, Tailwind e Vitest.

```
frontend/
  app/
    layout.tsx
    page.tsx                    Server Component: recebe searchParams e busca
    beneficiary-search-form.tsx Client Component: apenas o formulário
    beneficiary-result.tsx      Server Component: exibe o resultado
  lib/
    api.ts                      Cliente da API do backend
    types.ts                    Contratos de resposta
```

### Limites servidor/cliente

A página é Server Component e busca os dados com `await`. Somente o formulário
é `'use client'`, porque precisa de estado de digitação e alternância entre CPF
e NIS.

A URL da API fica em `API_URL`, variável de servidor. Não é usada
`NEXT_PUBLIC_`, para que o endereço do backend não vá ao navegador.

### Acessibilidade

- Cada campo tem `<label>` associado
- A escolha entre CPF e NIS usa `radiogroup` navegável por teclado
- A situação cadastral mostra código e descrição, nunca apenas cor
- Um único `<h1>` por página

### shadcn/ui

Os componentes de `shadcn/ui` são copiados para o repositório, não instalados
como dependência. Esta feature usa um conjunto mínimo escrito à mão com as
mesmas convenções de Tailwind, evitando trazer o CLI e suas dependências
transitivas sem um ADR que as justifique.

---

## Execução por Docker

Nenhum comando exige Node, Java ou banco instalados no host. O `compose.yaml`
ganha dois serviços:

| Serviço | Função |
|---|---|
| `frontend` | Executa o Next.js em modo de desenvolvimento |
| `frontend-test` | Executa o Vitest, no perfil `test` |

---

## Riscos

| Risco | Mitigação |
|---|---|
| A trilha de auditoria sem identificação de usuário pode dar falsa sensação de conformidade | Limitação declarada em `tasks.md` e no ADR de auditoria parcial |
| A correção da ordenação diverge do legado | O legado é internamente contraditório neste ponto; a divergência é documentada em `REQ-040` |
| O módulo de frontend aumenta a superfície de manutenção | Recorte mínimo: uma página, sem biblioteca de estado nem CLI de componentes |
