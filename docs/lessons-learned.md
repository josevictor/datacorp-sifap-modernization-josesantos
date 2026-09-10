# Lições aprendidas — Erros comuns dos times

![Tipo: referência](https://img.shields.io/badge/Tipo-Refer%C3%AAncia-171717?style=flat-square)
![Leitura de 5 minutos](https://img.shields.io/badge/Leitura-5%20min-737373?style=flat-square)

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Lições aprendidas**

**Um registro dos dez erros mais comuns observados em times anteriores**, com suas consequências e correções.

| Campo | Valor |
|---|---|
| **Público-alvo** | O time inteiro, especialmente o Technical Lead |
| **Quando ler** | Antes do início da imersão |
| **Resultado esperado** | Reconhecer padrões de falha e conhecer a correção antes que ela seja necessária |

---

## Os dez erros mais comuns

### 1. "Não precisamos inspecionar o sistema legado: o briefing é suficiente"

- **Consequência:** o time escreve EARS sem `source_legacy:`. A CI rejeita o pull request às 14:30. O time perde uma hora refazendo o trabalho.
- **Correção:** aplique o gate obrigatório do Estágio 1, que o facilitador valida às 13:50. Consulte [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md).

### 2. "Vou começar a programar enquanto outra pessoa escreve a especificação"

- **Consequência:** o código não corresponde aos requisitos EARS. A refatoração acontece no fim do dia. A demonstração fica incompleta.
- **Correção:** o Estágio 3 começa somente após o handoff H2. O Technical Lead interrompe tentativas de antecipar o trabalho.

### 3. O Product Owner aprova tudo e nada fica fora do escopo

- **Consequência:** o time tenta implementar 12 funcionalidades em três horas e não conclui nenhuma.
- **Correção:** o Product Owner recusa solicitações pelo menos três vezes durante o dia. Regra de decisão: _"Isso afeta o ciclo mensal de pagamentos? Sim → v1. Não → backlog."_

### 4. Cada pessoa usa o Copilot de uma forma diferente

- **Consequência:** as respostas são inconsistentes. O time debate com o assistente em vez de produzir artefatos.
- **Correção:** o time inteiro seleciona o mesmo agente de estágio (`@archaeologist`, `@architect` e assim por diante) no GitHub Copilot.

### 5. Pular `/speckit.clarify` para economizar tempo

- **Consequência:** as ambiguidades se tornam bugs no Estágio 3. Trinta minutos de perguntas agora evitam duas horas de retrabalho depois.
- **Correção:** cada pergunta de `clarify` representa um bug evitado. Responda a todas.

### 6. Executar `git push --force` em `develop`

- **Consequência:** o trabalho de duas pessoas é perdido sem um caminho simples de recuperação.
- **Correção:** proteja `develop` (Passo 4 de `00-SETUP.md`). Nunca use `--force` em uma branch compartilhada.

### 7. Editar uma migração antiga em vez de criar uma nova

- **Consequência:** o Flyway detecta uma divergência de checksum e o banco de dados deixa de iniciar.
- **Correção:** nunca edite um arquivo de migração aplicado. Sempre crie `V<N+1>__description.sql`. Consulte [`docs/troubleshooting.md`](troubleshooting.md).

### 8. Delegar uma Issue vaga ao Copilot Agent

- **Consequência:** o pull request gerado não pode ser usado e o trabalho é descartado.
- **Correção:** vincule a Issue às evidências e escreva critérios de aceitação verificáveis antes de delegar. Uma Issue bem escrita produz um pull request utilizável.

### 9. Executar `terraform apply` em vez de `plan`

- **Consequência:** os recursos do Azure são criados e cobrados imediatamente. A imersão não autoriza `apply`.
- **Correção:** execute somente `terraform plan`. Consulte [`04-evolution/GUIDE.md`](../04-evolution/GUIDE.md).

### 10. Não ensaiar a demonstração

- **Consequência:** o time gasta os três minutos da demonstração procurando a aba correta, um comando que falhou ou um pull request perdido.
- **Correção:** o período de 16:50–17:00 é reservado para o ensaio. Use [`demo-script.md`](demo-script.md).

---

## Cinco hábitos que distinguem bons times de times excelentes

1. **Stand-up de dois minutos** no fim de cada estágio: todos conhecem o estado atual.
2. **Todo pull request tem uma descrição**: use o modelo do GitHub.
3. **Commits pequenos incluem um REQ-ID** na mensagem de commit.
4. **A regra dos 20 minutos**: está bloqueado? Peça ajuda. Não enfrente o problema em silêncio.
5. **Confie no processo**: não invente um workflow diferente no meio do dia.

---

## A regra fundamental

> **Modernização é arqueologia digital, não um projeto greenfield.**
> Um time que trata o SIFAP como um sistema novo perde 29 anos de regras de negócio.
> Um time que realiza primeiro a arqueologia entrega um SIFAP 2.0 capaz de realmente substituir a versão 1.0.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Checklist do líder](CHECKLIST-LIDER.md)<br/><sub>Verificações hora a hora para o dia.</sub> | [Roteiro da demonstração](demo-script.md)<br/><sub>Roteiro para os minutos finais.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
