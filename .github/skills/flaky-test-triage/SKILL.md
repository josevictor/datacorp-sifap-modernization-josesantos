---
name: "flaky-test-triage"
description: "Use quando um teste for intermitente, a integração contínua (CI) estiver instável ou for necessário colocar um teste instável em quarentena. Os gatilhos incluem \"teste instável\", \"quarentena\", \"falha intermitente\", \"instabilidade da CI\" e \"painel de testes instáveis\"."
---
# Triagem de testes instáveis

## Quando usar

- A CI falha e a nova execução passa.
- "Este teste é instável. Ajude-me a corrigi-lo."
- "Crie um processo de quarentena para testes instáveis."

## Fluxo de diagnóstico

1. **Reproduza**: execute o teste isoladamente 50 vezes com `--repeat-each 50` (Playwright) ou `pytest --count=50`. Se ele falhar menos de uma vez, provavelmente depende da ordem de execução.
2. **Categorize** a causa raiz da instabilidade:

- **Assincronismo/temporização**: ausência de `await`, condição de corrida, `sleep` fixado no código
- **Dependência de ordem**: estado compartilhado, banco de dados não limpo, instância única global
- **Dependência externa**: rede, relógio, sistema de arquivos
- **Não determinismo**: iteração em mapa não ordenado, semente aleatória
- **Disputa de recursos**: porta, bloqueio de arquivo, colisão entre processos paralelos

3. **Corrija a causa raiz**: substitua chamadas de `sleep` por esperas explícitas, isole o estado, defina sementes aleatórias e use portas com escopo de teste.
4. **Coloque em quarentena se não puder corrigir em menos de um dia**: aplique a etiqueta `flaky/`, abra um item de acompanhamento no GitHub e defina um acordo de nível de serviço (SLA) de 30 dias para corrigi-lo ou excluí-lo.

## Política de quarentena

- Os testes em quarentena são executados, mas não causam falha na compilação.
- Exclua tudo que permanecer em quarentena por mais de 30 dias. Um teste que não pode ser corrigido é pior do que não ter teste.
- Painel: acompanhe a taxa de instabilidade de cada teste em 100 execuções. Coloque automaticamente em quarentena tudo que superar 5%.

## Antipadrões

- `sleep(1000)`: sempre incorreto.
- Repetir a asserção em um laço: oculta erros de temporização.
- `@Retry(3)`: mascara instabilidades e favorece testes de baixa qualidade.

## Modelo de saída

Registre cada instabilidade investigada e sua resolução:

```markdown
## Triagem de instabilidade: <id do teste>

| Campo | Valor |
|---|---|
| Teste | <suíte::nome do teste> |
| Taxa de instabilidade | <N>% em <M> execuções |
| Causa raiz | Assincronismo-temporização / Dependência de ordem / Dependência externa / Não determinismo / Disputa de recursos |
| Correção ou quarentena | <hiperlink da solicitação de alteração (PR) ou etiqueta `flaky/` + item de acompanhamento> |
| SLA | <data-limite de 30 dias para corrigir ou excluir> |

### Evidências
- <comando usado para reproduzir, por exemplo: pytest --count=50 path::test>
- <saída de falha ou condição de corrida observada>
```

## Critérios de qualidade

- [ ] A instabilidade foi reproduzida isoladamente (mais de 50 execuções) e sua categoria foi identificada.
- [ ] A correção trata a causa raiz, sem adicionar `sleep`, nova tentativa nem laço de asserção.
- [ ] Tudo que não for corrigido em um dia entra em quarentena com um item de acompanhamento no GitHub e um SLA de 30 dias.
- [ ] Os testes em quarentena continuam sendo executados, mas não causam falha na compilação.

## Referências

- [Google: Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)
- [Microsoft Research: Empirical Study of Flaky Tests](https://www.microsoft.com/en-us/research/publication/an-empirical-analysis-of-flaky-tests/)
