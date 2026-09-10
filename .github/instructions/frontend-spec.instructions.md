---
description: "Use ao implementar ou revisar Next.js 15 App Router, TypeScript, Tailwind CSS, shadcn/ui e server components em frontend/."
applyTo: "frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**,frontend/**/*.ts,frontend/**/*.tsx"
---

# Especificação de frontend — Next.js 15 + TypeScript

Este arquivo é ativado ao trabalhar com TypeScript, TSX, rotas App Router ou componentes reutilizáveis em `frontend/`. Ele ensina o contrato de plataforma do SIFAP modernizado (Sistema de Fiscalização e Administração de Pagamentos): Next.js 15 App Router, Server Components, Server Actions, TypeScript strict, Tailwind CSS, shadcn/ui, base de acessibilidade e integração com Vitest. Ele rege framework, tipagem, estilo e limites servidor/cliente; [`frontend.instructions.md`](frontend.instructions.md) rege construção de componentes, detalhes de interação no cliente, coordenação de estado, execução de acessibilidade e fluxos voltados às pessoas usuárias.

## Resumo da stack

| Camada | Tecnologia | Versão |
|-------|-----------|---------|
| Framework | Next.js (App Router) | 15 |
| Linguagem | TypeScript (modo strict) | 5+ |
| Estilo | Tailwind CSS | 3.4+ |
| Componentes | shadcn/ui | Mais recente |
| Estado (cliente) | React `useState` e Context quando necessário | Nativo |
| Dados do servidor | Server Components e Server Actions | Nativo |
| Testes | Vitest + Testing Library | Mais recente |

## Padrões do App Router

### Server Components (padrão)

Todo componente é um Server Component, salvo quando explicitamente marcado de outra forma. Server Components:

- Executam no servidor e nunca enviam JS ao cliente
- Podem usar `await` diretamente para buscar dados
- Não podem usar hooks, handlers de eventos ou APIs do navegador

```tsx
// app/<resource>/page.tsx — Server Component (padrão)
export default async function ResourcePage() {
  const response = await fetch('/api/v1/<resource>');
  if (!response.ok) throw new Error('Falha ao carregar o recurso');
  const resources = await response.json();
  return <ResourceList resources={resources} />;
}
```

### Client Components

Adicione `'use client'` somente quando houver necessidade de interatividade:

```tsx
'use client';

import { useState } from 'react';

export function ResourceFilter({ onFilter }: { onFilter: (term: string) => void }) {
  const [term, setTerm] = useState('');
  return (
    <input
      value={term}
      onChange={e => { setTerm(e.target.value); onFilter(e.target.value); }}
      placeholder="Filtrar recursos..."
    />
  );
}
```

Regras:

- **Reduza a superfície `'use client'`**: leve a interatividade ao menor componente possível. Uma página que busca dados DEVE ser um Server Component; somente o filtro/formulário interativo dentro dela DEVE ser um Client Component.
- **NUNCA exponha segredos em componentes cliente**: chaves de API, tokens e URLs internas DEVEM permanecer no servidor.
- **Evite dependências de estado por padrão**: use `useState` local e Context para estado compartilhado no cliente. Adicione uma biblioteca de estado ou cache somente com um ADR que justifique a dependência.

### Server Actions para mutações

Use server actions em vez de manipuladores de rotas de API no envio de formulários:

```tsx
// app/<resource>/actions.ts
'use server';

export async function createResource(formData: FormData) {
  const value = formData.get('value');
  // Valida e chama a API do backend
  const res = await fetch(`${process.env.API_URL}/api/v1/<resource>`, {
    method: 'POST',
    body: JSON.stringify({ value }),
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) throw new Error('Falha ao criar o recurso');
}
```

## Convenções de TypeScript

- **`strict: true`** em `tsconfig.json`: sem exceções e sem `// @ts-ignore`
- **Sem `any`**: use `unknown` e restrinja-o com type guards
- **Somente exports nomeados em componentes reutilizáveis**: `export function ResourceCard()`. Arquivos de rota do App Router podem usar o `export default` exigido pelo Next.js.
- **Interface em vez de type** para formatos de objeto extensíveis
- **Utility types**: use `Pick`, `Omit` e `Partial` em vez de duplicar interfaces

```tsx
// Correto: export nomeado e props tipadas
export function ResourceCard({ resource }: { resource: ResourceDto }) {
  return <div>{resource.label}</div>;
}

// Errado: export default e tipo any
export default function ResourceCard({ resource }: { resource: any }) { ... }
```

## Tailwind CSS + shadcn/ui

- Use classes utilitárias Tailwind diretamente; não crie arquivos CSS separados, salvo quando indispensável
- Use componentes shadcn/ui para elementos padrão de IU (Button, Card, Table, Dialog etc.)
- Quando a equipe definir tokens do design system, use-os para cores e espaçamento
- Responsivo por padrão: mobile-first com breakpoints `sm:`, `md:` e `lg:`

```tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function ResourceSummary({ total }: { total: number }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Resumo dos recursos</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-2xl font-bold">{total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</p>
      </CardContent>
    </Card>
  );
}
```

## Base de acessibilidade

Toda página e componente DEVE atender a estes requisitos mínimos:

- Todas as imagens possuem texto `alt`
- Entradas de formulário possuem elementos `<label>` associados
- Elementos interativos podem ser navegados por teclado
- A cor não é o único meio de transmitir informações
- A página possui um único `<h1>`, e os títulos seguem uma ordem lógica

## Testes com Vitest

```tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { ResourceCard } from './ResourceCard';

describe('ResourceCard', () => {
  it('displays the resource label when a resource is provided', () => {
    render(<ResourceCard resource={{ label: 'Example' }} />);
    expect(screen.getByText('Example')).toBeInTheDocument();
  });
});
```

Nome do teste: `should_[expected behavior]_when_[condition]` ou `displays [what] when [condition]`.

## Convenções

| Regra | Justificativa |
|---|---|
| Next.js 15 App Router com Server Components por padrão | Reduz JavaScript no cliente e mantém o acesso a dados no servidor |
| `strict: true`, sem `any` e sem `// @ts-ignore` | Erros de tipo aparecem antes da execução |
| Exports nomeados em componentes reutilizáveis | Imports consistentes; arquivos de rota mantêm defaults exigidos |
| Server Actions para mutações | Formulários fazem mutações por um limite de servidor |
| Tailwind CSS e shadcn/ui para IU | Evita stacks de estilo ad hoc e mantém componentes consistentes |
| Vitest + Testing Library com nomes focados em comportamento | Testes descrevem comportamento visível e condições esperadas |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Use exports nomeados em arquivos de componentes | Use `export default` em componentes reutilizáveis |
| Use `unknown` com type guards | Use `any` ou suprima TypeScript strict |
| Use `async`/`await` em fluxos assíncronos | Encadeie chamadas `.then()` |
| Estilize com Tailwind e shadcn/ui | Adicione módulos CSS ou styled-components |
| Busque diretamente com `await` em Server Components | Adicione busca de dados no cliente a Server Components |
| Mantenha segredos no servidor | Coloque segredos em arquivos `'use client'` ou variáveis `NEXT_PUBLIC_` |

## Lista de verificação antes de abrir uma PR

- [ ] `tsconfig.json` permanece strict; nenhum `any` ou `// @ts-ignore` foi adicionado
- [ ] Server Components continuam sendo o padrão, e `'use client'` aparece somente onde a interação o exige
- [ ] Mutações usam Server Actions e validam dados antes de chamar a API do backend
- [ ] Componentes reutilizáveis usam exports nomeados; arquivos de rota usam defaults somente quando exigidos pelo Next.js
- [ ] O estilo usa utilitários Tailwind e componentes shadcn/ui sem nova dependência de estilo
- [ ] A base de acessibilidade está coberta: labels, operação por teclado, ordem de títulos e sinais além de cor
- [ ] Testes Vitest + Testing Library cobrem o comportamento alterado com o padrão de nomenclatura acordado
