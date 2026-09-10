---
name: "playwright-generate-test"
description: "Gera um teste de ponta a ponta com Playwright em TypeScript a partir de um cenário descrito, conduzindo o Playwright MCP passo a passo e executando o teste até que passe. Use quando a pessoa solicitar a criação ou gravação de um teste de navegador ou E2E com Playwright para um fluxo web."
---
# Geração de testes de ponta a ponta com Playwright

Gere um teste de ponta a ponta (E2E) com Playwright em TypeScript explorando o fluxo de usuário descrito com o servidor Playwright MCP, uma etapa por vez. Em seguida, produza uma especificação `@playwright/test` e execute-a até que passe. Esta habilidade abrange testes de regressão no nível do navegador para a interface do SIFAP 2.0 em Next.js 15. O comportamento unitário e de componentes permanece no Vitest + Testing Library (consulte [`tests.instructions.md`](../../instructions/tests.instructions.md)).

> [!NOTE]
> Esta habilidade conduz o **servidor Playwright MCP**, que deve estar instalado e em execução contra uma interface acessível. Se o servidor MCP estiver indisponível, instale-o e inicie-o antes de usar a habilidade. Não escreva o teste manualmente apenas com base no cenário.

## Quando invocar

- "Gere um teste Playwright para o fluxo de aprovação de pagamento."
- "Grave um teste de ponta a ponta que faça login e abra o painel."
- "Crie um teste de regressão de navegador para este cenário."
- "Transforme esta jornada de usuário em uma especificação Playwright."

## Fluxo explorar e depois gerar

Nunca escreva o código do teste apenas com base na descrição do cenário. Primeiro, observe o DOM real por meio do MCP e depois gere o teste.

1. **Obtenha o cenário.** Se a pessoa não descrever um fluxo, solicite-o. Confirme a URL base da interface em execução.
2. **Explore passo a passo.** Conduza o fluxo, uma ação por vez, com as ferramentas do Playwright MCP (navegar, clicar, preencher e verificar). Use cada estado observado da página para orientar a próxima etapa.
3. **Prefira localizadores acessíveis.** Selecione elementos por função, rótulo ou texto (`getByRole`, `getByLabel`), não por CSS frágil ou `data-testid` quando houver uma função. Isso segue a convenção do Testing Library usada no restante do kit.
4. **Gere a especificação.** Somente depois de confirmar todas as etapas, produza um teste TypeScript com `@playwright/test` com base nas interações registradas. Estruture-o como Preparar-Agir-Verificar e adicione um comentário na mesma linha `// REQ-NNN` quando o fluxo rastrear até um requisito.
5. **Salve-o** no diretório `tests/` da interface como `<feature>.spec.ts`.
6. **Execute e ajuste.** Execute `npx playwright test <name>` e corrija localizadores ou esperas até o teste passar de forma confiável. Nunca deixe uma especificação com falha ou instável.

> [!WARNING]
> Não inclua segredos nem dados específicos do ambiente na especificação. Leia URLs base e credenciais de variáveis de ambiente ou da configuração do Playwright. Nunca os fixe no código.

## Limites do escopo

| Camada | Ferramenta | Responsável |
|---|---|---|
| Ponta a ponta (navegador) | Playwright | esta habilidade |
| Componente / interação | Vitest + Testing Library | [`tests.instructions.md`](../../instructions/tests.instructions.md) |
| Unitária / lógica pura | Vitest (interface) ou JUnit 5 (camada de servidor) | [`test-strategy`](../test-strategy/SKILL.md) |

## Modelo de saída

```typescript
import { test, expect } from '@playwright/test';

// REQ-XXX: uma pessoa analista aprova um pagamento pendente
test('analista aprova um pagamento pendente', async ({ page }) => {
  await page.goto('/payments');                                    // Preparar

  await page
    .getByRole('row', { name: /pending/i })
    .first()
    .getByRole('link', { name: /review/i })
    .click();

  await page.getByRole('button', { name: /approve/i }).click();    // Agir

  await expect(page.getByRole('status')).toHaveText(/approved/i);  // Verificar
});
```

Resultado da execução a informar:

```text
npx playwright test payment-approval
  1 passed (2.1s)
```

## Critérios de qualidade

- [ ] O fluxo foi explorado passo a passo pelo Playwright MCP antes da escrita do código.
- [ ] A especificação usa `@playwright/test` e está no diretório `tests/` da interface.
- [ ] Os elementos são selecionados por função ou rótulo acessível, não por seletores frágeis.
- [ ] Os fluxos orientados por requisitos contêm um comentário na mesma linha `// REQ-NNN`.
- [ ] O teste passa e não é instável; nenhum segredo está fixado no código.
- [ ] A cobertura unitária e de componentes permanece no Vitest + Testing Library.
