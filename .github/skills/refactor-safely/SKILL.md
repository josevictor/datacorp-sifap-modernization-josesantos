---
name: "refactor-safely"
description: "Use ao refatorar código legado, extrair um serviço ou fazer alterações que preservem o comportamento. Os gatilhos incluem \"refatorar\", \"código legado\", \"padrão Estrangulador (Strangler Fig)\", \"teste de caracterização\" e \"Método Mikado\"."
---
# Refatoração segura

## Quando invocar

- Ao trabalhar em código sem testes suficientes.
- Ao dividir um monólito ou extrair um serviço.
- Quando uma alteração tem "uma linha", mas afeta um fluxo arriscado.

## Primeira regra

**A refatoração preserva o comportamento.** Se você não puder provar que o comportamento foi preservado, não é refatoração, mas reescrita. Primeiro, implemente testes de caracterização.

## Fluxo de trabalho

1. **Caracterize**: escreva testes que fixem o comportamento atual, inclusive suas peculiaridades. Ainda não corrija bugs. O objetivo é criar uma rede de segurança, não uma correção.
2. **Dê passos pequenos e reversíveis**: aplique uma transformação que preserve o comportamento por vez. Faça um registro de alteração após cada uma.
3. **Mantenha os testes verdes**: execute-os após cada etapa. Reverta imediatamente se ficarem vermelhos e você não souber o motivo.
4. **Separe registros de refatoração dos registros que alteram o comportamento**: as pessoas revisoras poderão manter o foco, e o `git bisect` continuará útil.
5. **Integre com frequência**: ramificações de refatoração de longa duração se deterioram.

## Padrões

### Padrão Estrangulador (Strangler Fig) para sistemas

1. Coloque uma fachada (intermediário, também chamado de proxy, roteador ou chave de funcionalidade) à frente do sistema antigo.
2. Direcione uma pequena parcela do tráfego para a nova implementação.
3. Amplie a nova implementação por partes enquanto reduz a antiga.
4. Exclua a implementação antiga quando seu tráfego chegar a zero.

### Método Mikado (para código)

1. Registre o objetivo.
2. Tente alcançá-lo diretamente e registre o que falhar como **pré-requisito**.
3. Reverta. Resolva primeiro um pré-requisito. Repita recursivamente.
4. Conclua primeiro as folhas e alcance o objetivo original por último.

### Ramificação por abstração (Branch by Abstraction)

Introduza uma interface, migre as partes chamadoras para ela, troque as implementações e desative a antiga, tudo sem uma ramificação de longa duração.

## Como criar testes de caracterização

- Execute o código com entradas representativas e registre a saída (arquivos de referência ou testes de instantâneo).
- Prefira observar externamente (HTTP, CLI ou estado do banco de dados). Essa abordagem resiste a refatorações internas.
- Cubra também casos incomuns, pois eles costumam falhar.
- Aceite que alguns comportamentos são *erros que agora estão sendo preservados*. Marque-os e corrija-os depois que a rede de segurança estiver pronta.

## Antipadrões

- Solicitações de pull de "refatoração" que também corrigem erros, alteram APIs e renomeiam arquivos, o que impossibilita a revisão e a reversão.
- Reescritas integrais sem entregas durante meses.
- Exclusão do código antigo antes de o novo código processar 100% do tráfego.
- Refatoração sem testes, baseada apenas na verificação manual do fluxo de sucesso.

## Modelo de saída

```markdown
## Plano de refatoração - <alvo>

| Campo | Valor |
|---|---|
| Objetivo | <alteração que preserva o comportamento> |
| Rede de segurança | <caminho do teste de caracterização> |
| Padrão | Estrangulador / Mikado / Ramificação por abstração |
| Etapas | <transformações ordenadas e reversíveis> |

### Pré-requisitos (Mikado)
- <pré-requisito descoberto ao tentar alcançar o objetivo>

### Registros de alteração
- refactor: <uma etapa que preserva o comportamento por commit>
```

## Critérios de qualidade

- [ ] Os testes de caracterização capturam o comportamento atual, inclusive peculiaridades, antes de qualquer alteração.
- [ ] Os registros de refatoração estão separados dos registros que alteram o comportamento.
- [ ] Os testes permanecem verdes após cada etapa; uma etapa vermelha é revertida, não forçada.
- [ ] O código antigo só é excluído depois que o novo fluxo processa todo o tráfego.

## Referências

- [Martin Fowler - Refactoring (2nd ed.)](https://martinfowler.com/books/refactoring.html)
- [Michael Feathers - Working Effectively with Legacy Code](https://www.oreilly.com/library/view/working-effectively-with/0131177052/)
- [Mikado Method](https://mikadomethod.info/)
- [Fowler - Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html)
