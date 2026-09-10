# Catálogo de Regras de Negócio — SIFAP Legado

> **Trilha:** [Kit do Time](../README.md) › [Estágio 1](README.md) › **Catálogo de Regras de Negócio**

**Artefato preenchido pelo time durante o Estágio 1.** Cada dupla extrai as regras dos programas `.NSP` e `.NSN` que recebeu e as registra aqui, com rastreabilidade obrigatória até o programa de origem.

| Campo | Valor |
|---|---|
| **Público-alvo** | Todas as duplas — cada dupla preenche a seção dos seus programas |
| **Pré-requisitos** | Ler os programas `.NSP` e `.NSN` atribuídos |
| **Estágio** | Estágio 1 — Arqueologia |
| **Resultado esperado** | Catálogo com `Programa de origem` preenchido para cada regra candidata |

> [!NOTE]
> Cada regra cita o programa de origem com um intervalo de linhas (`arquivo.NSP:Linicio-Lfim` ou `arquivo.NSN:Linicio-Lfim`) e é classificada como **Confirmada** (corroborada pela documentação histórica em `legacy-sifap/legacy-docs/`), **Inferida** (só a partir do código) ou **Mistério** (questão em aberto — registre-a também em [`mysteries-found.md`](mysteries-found.md) com evidência `path:line`, hipótese não confirmada, responsável e status).

> [!IMPORTANT]
> Guia passo a passo: [`GUIDE.md`](GUIDE.md).

**Time**: <!-- preencher -->

---

## Regras de `<preencher: PROGRAMA.NSP ou PROGRAMA.NSN>`

| # | Enunciado da regra | Candidato EARS | Origem | Classificação | Notas |
|---|---|---|---|---|---|
| 1 | <!-- preencher --> | <!-- preencher: padrão EARS --> | <!-- preencher: arquivo:linha --> | <!-- preencher: Confirmada/Inferida/Mistério --> | <!-- preencher --> |

> [!NOTE]
> Duplique a seção acima para cada programa `.NSP` ou `.NSN` lido pela sua dupla.

---

## Resumo geral

| Métrica | Valor |
|---|---:|
| Programas Natural lidos | <!-- preencher --> |
| DDMs cruzados | <!-- preencher --> |
| Regras confirmadas | <!-- preencher --> |
| Regras inferidas | <!-- preencher --> |
| Mistérios | <!-- preencher --> |

---

## Definição de pronto

- [ ] Todo bloco condicional dos programas atribuídos foi examinado.
- [ ] Toda regra cita `arquivo:linha`.
- [ ] Toda questão em aberto está registrada em `mysteries-found.md` sem conclusão.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Inventário](inventory.md)<br/><sub>Passo 1 — varredura de arquivos.</sub> | [Mapa de Dependências](dependency-map.md)<br/><sub>Passo 3 — grafo de chamadas e acessos.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
