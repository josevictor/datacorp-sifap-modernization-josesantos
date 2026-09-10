# FAQ — Perguntas frequentes

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **FAQ**

**Respostas diretas às perguntas comuns sobre a imersão de modernização do SIFAP.**

| Campo | Valor |
|---|---|
| **Público-alvo** | O time inteiro |
| **Como usar** | Pesquise a pergunta com `Ctrl+F`. Se ela não estiver aqui, consulte [troubleshooting.md](troubleshooting.md) |
| **Tempo estimado** | Leitura seletiva |

---

## Sobre a imersão

<details>
<summary><strong>Eu não programo. Posso participar?</strong></summary>

Sim. As personas Product Owner e Tech Writer, além de parte de QA, não exigem programação. Leia primeiro [`07-concepts/`](../07-concepts/) para conhecer os conceitos. Todo `PERSONA.md` inclui uma seção "emergency defaults".

</details>

<details>
<summary><strong>Quanto tempo dura?</strong></summary>

Oito horas (10:00–18:00). O cronograma exato está em [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md) §2.

</details>

<details>
<summary><strong>Quantas pessoas há em cada time?</strong></summary>

Cinco. Cada pessoa assume duas personas (uma dupla), cobrindo dez personas no total.

</details>

<details>
<summary><strong>Posso escolher minhas duas personas?</strong></summary>

Sim, mas coordene com o time. As Duplas 1, 4 e 5 acomodam perfis não técnicos. As Duplas 2 e 3 exigem experiência técnica.

</details>

<details>
<summary><strong>O que é o SIFAP?</strong></summary>

O SIFAP (Sistema de Fiscalização e Administração de Pagamentos) é um sistema governamental de pagamentos com 29 anos, escrito em Natural/Adabas. A imersão simula sua modernização para Java 21 + Next.js 15. Consulte [`01-archaeology/legacy-sifap/README.md`](../01-archaeology/legacy-sifap/README.md).

</details>

---

## Sobre o Copilot

<details>
<summary><strong>Qual modelo do Copilot devo usar?</strong></summary>

Sonnet 4.6 para a maioria das tarefas. Haiku para tarefas mecânicas e repetitivas. Opus para decisões arquiteturais complexas. Consulte [`09-cheat-sheets/model-routing.md`](../09-cheat-sheets/model-routing.md).

</details>

<details>
<summary><strong>Quando devo usar Ask, Plan ou Agent?</strong></summary>

- **Ask** — discutir e entender.
- **Plan** — planejar uma mudança em vários arquivos.
- **Agent** — delegar uma Issue completa.

Referência: [`07-concepts/04-3-copilot-modes.md`](../07-concepts/04-3-copilot-modes.md).

</details>

<details>
<summary><strong>O Agent pode fazer merge sozinho?</strong></summary>

Não. O Agent abre um pull request. Revise-o com o mesmo cuidado aplicado a uma contribuição humana.

</details>

<details>
<summary><strong>Posso usar Cursor, Codeium ou outro assistente?</strong></summary>

Não. O conjunto de ferramentas é fixo: use somente o GitHub Copilot. Consulte [`.github/copilot-instructions.md`](../.github/copilot-instructions.md).

</details>

---

## Sobre Spec-Kit e EARS

<details>
<summary><strong>Por que todo requisito EARS precisa de `source_legacy:`?</strong></summary>

Para garantir que o time modernizou o sistema real, não apenas o briefing. A CI rejeita pull requests sem esse campo. Consulte [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md).

</details>

<details>
<summary><strong>E se a funcionalidade for nova e não tiver equivalente no legado?</strong></summary>

Use `source_legacy: "[GREENFIELD] <justificativa de uma linha>"`. Exemplo: `"[GREENFIELD] OAuth2 não existia em um terminal 3270."`.

</details>

<details>
<summary><strong>Posso pular `/speckit.clarify`?</strong></summary>

Não. Pulá-lo faz com que as ambiguidades se tornem bugs no Estágio 3, quando custam muito mais para corrigir.

</details>

<details>
<summary><strong>`/speckit.analyze` relata problemas. O que devo fazer?</strong></summary>

Resolva-os antes da implementação. Cada descoberta evita retrabalho posterior.

</details>

---

## Sobre Git e branches

<details>
<summary><strong>Posso fazer commit diretamente em `main`?</strong></summary>

Não. Sempre use um pull request. Consulte a regra 1 em [`00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md).

</details>

<details>
<summary><strong>Qual prefixo de branch devo usar?</strong></summary>

- `spec/<NNN>-<feature>` no Estágio 2
- `impl/<NNN>-<feature>` no Estágio 3
- `infra/<component>` para infraestrutura

As duas branches de funcionalidade partem de `develop`. Consulte a tabela completa em [`00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md).

</details>

<details>
<summary><strong>Como meu PR é aprovado?</strong></summary>

CI verde e uma revisão da dupla que recebe. O fluxo é Dupla 1 → Dupla 2 → Dupla 3 → Dupla 4 → Dupla 5 → Dupla 1.

</details>

<details>
<summary><strong>Posso executar `git push --force`?</strong></summary>

Somente na sua própria branch e apenas com `--force-with-lease`. Nunca em `develop` ou `main`.

</details>

---

## Sobre Terraform e Azure

<details>
<summary><strong>Posso executar `terraform apply`?</strong></summary>

> [!CAUTION]
> Não. Somente `terraform plan` é autorizado durante a imersão. Executar `apply` cria recursos reais do Azure e gera custos.

</details>

<details>
<summary><strong>Onde devo armazenar segredos?</strong></summary>

No Azure Key Vault. Nunca em `variables.tf` ou arquivos `.env` versionados. Ao criar `infra/`, modele os segredos com o Key Vault e a Managed Identity.

</details>

---

## Sobre estágios e handoffs

<details>
<summary><strong>O que são os "handoffs H1, H2 e H3"?</strong></summary>

São pontos de transferência de artefatos entre duplas no fim de cada estágio. Cada handoff é uma conversa síncrona de cinco minutos. Os detalhes estão em [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md) §3.

</details>

<details>
<summary><strong>Posso começar o Estágio 2 enquanto o Estágio 1 ainda está em andamento?</strong></summary>

Não. Sem concluir a arqueologia do Estágio 1, os requisitos EARS não terão `source_legacy:` e a CI rejeitará o pull request.

</details>

<details>
<summary><strong>Quem lidera cada estágio?</strong></summary>

Consulte [`05-personas/OVERVIEW.md`](../05-personas/OVERVIEW.md). Resumo:

- Estágio 1 — todas as duplas em paralelo
- Estágio 2 — Dupla 2
- Estágio 3 — Duplas 3 e 4
- Estágio 4 — Dupla 5

</details>

---

## Sobre bloqueios

<details>
<summary><strong>Estou bloqueado. O que devo fazer?</strong></summary>

Use a regra dos 20 minutos ([`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md) §6):

| Tempo bloqueado | Ação |
|---|---|
| 5 min | Tente resolver por conta própria |
| 10 min | Peça ajuda à sua dupla |
| 20 min | Leve o problema ao time |
| 30 min | Peça ajuda ao facilitador |

</details>

<details>
<summary><strong>Como peço ajuda de forma eficiente?</strong></summary>

Use três linhas: (1) Objetivo, (2) O que tentei, (3) Bloqueio. Consulte o exemplo em [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md) §6.

</details>

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Solução de problemas](troubleshooting.md)<br/><sub>Erros comuns e soluções.</sub> | [Kit em pt-BR](../README.md)<br/><sub>Ponto de entrada principal.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
