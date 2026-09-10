---
description: "Use ao criar componentes de IU de frontend, páginas, interações no cliente, estado de componentes, acessibilidade e fluxos voltados às pessoas usuárias."
applyTo: "frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**"
---

# Convenções de frontend — Construção de componentes e interação

Este arquivo é ativado quando você cria IU em `frontend/app/**` ou `frontend/components/**`. Ele se concentra na construção de componentes, interação no cliente, estado de componentes, execução de acessibilidade e fluxos voltados às pessoas usuárias. Ele rege o comportamento dos componentes; [`frontend-spec.instructions.md`](frontend-spec.instructions.md) rege o contrato de plataforma para Next.js 15 App Router, TypeScript strict, estilo Tailwind/shadcn, Server Components e Server Actions. Siga esse arquivo para esses tópicos e não os repita aqui.

> [!NOTE]
> `frontend/` ainda não existe; a equipe cria sua estrutura no Estágio 3. Estas são as convenções que os componentes devem seguir desde sua criação.

## Construção de componentes

Crie componentes pequenos e com responsabilidade única, exports nomeados e props tipadas. Prefira composição a uma lista crescente de props e mantenha componentes de apresentação sem busca de dados.

```tsx
import type { ResourceDto } from '@/types/resource';

export function ResourceCard({ resource }: { resource: ResourceDto }) {
  return (
    <article className="rounded-lg border p-4">
      <h3 className="font-semibold">{resource.label}</h3>
      <p className="text-muted-foreground">{formatBRL(resource.amount)}</p>
    </article>
  );
}
```

Mantenha a superfície `'use client'` o menor possível: um Server Component busca os dados e os passa a um Client Component pequeno que trata a interação (consulte [`frontend-spec.instructions.md`](frontend-spec.instructions.md)).

## Estado de componentes

Use `useState` local por padrão. Eleve o estado ao ancestral comum mais próximo quando componentes irmãos precisarem compartilhá-lo. Use Context **somente** para estado de cliente realmente compartilhado e adicione uma biblioteca de gerenciamento de estado apenas com um ADR que justifique a dependência.

```tsx
'use client';

import { useState } from 'react';

export function ResourceFilter({ onFilter }: { onFilter: (term: string) => void }) {
  const [term, setTerm] = useState('');
  return (
    <label className="flex flex-col gap-1">
      <span>Filtrar recursos</span>
      <input
        value={term}
        onChange={(event) => { setTerm(event.target.value); onFilter(event.target.value); }}
      />
    </label>
  );
}
```

As entradas são controladas (`value` + `onChange`). Derive valores durante a renderização em vez de espelhar props no estado.

## Interação no cliente e fluxos assíncronos

As mutações passam por server actions, não por `fetch` no cliente (consulte [`frontend-spec.instructions.md`](frontend-spec.instructions.md)). Envolva a chamada em `useTransition` para controlar o estado desabilitado/pendente e reflita-o com `aria-busy`.

```tsx
'use client';

import { useTransition } from 'react';
import { Button } from '@/components/ui/button';

export function ArchiveButton({ id, onArchive }: { id: string; onArchive: (id: string) => Promise<void> }) {
  const [isPending, startTransition] = useTransition();
  return (
    <Button
      type="button"
      disabled={isPending}
      aria-busy={isPending}
      onClick={() => startTransition(() => onArchive(id))}
    >
      {isPending ? 'Arquivando…' : 'Arquivar'}
    </Button>
  );
}
```

## Fluxos voltados às pessoas usuárias

Toda tela assíncrona renderiza três estados explícitos, **carregamento**, **vazio** e **erro**, nunca uma tela em branco. Confirme ações destrutivas e formate valores e datas com um locale explícito para que a saída seja determinística.

```tsx
if (isLoading) return <Spinner aria-label="Carregando recursos" />;
if (resources.length === 0) return <EmptyState message="Ainda não há recursos" />;
if (error) return <ErrorState onRetry={refetch} />;
```

## Acessibilidade (WCAG 2.1 AA)

| Requisito | Como atendê-lo |
|---|---|
| Labels | Toda entrada possui `<label htmlFor>` ou `aria-label` |
| Teclado | Todos os elementos interativos podem ser alcançados e operados por Tab/Enter/Espaço |
| Foco | Mova o foco para o diálogo ao abrir e devolva-o ao acionador ao fechar |
| Contraste | Texto ≥ 4,5:1, texto grande ≥ 3:1 |
| Estrutura | Um `<h1>` por página, ordem lógica de títulos e regiões de referência |
| Cor | Nunca é o único sinal; combine-a com texto ou ícone |

Use elementos semânticos (`<button>`, `<nav>`, `<table>`) antes de recorrer a ARIA; adicione ARIA somente quando faltar semântica nativa.

## Convenções

| Regra | Justificativa |
|---|---|
| Exports nomeados para componentes | Imports consistentes e compatíveis com tree shaking |
| Props tipadas, sem `any` | Falhas aparecem na compilação |
| `useState` local, Context somente quando compartilhado | Grafo de estado mínimo e previsível |
| Coloque o teste ao lado do componente | Comportamento e cobertura permanecem juntos |
| Estados explícitos de carregamento/vazio/erro | Sem becos sem saída na IU |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Leve `'use client'` à menor folha | Marque uma página inteira com `'use client'` |
| Faça mutações por uma server action | Use `fetch` para uma mutação no cliente |
| Rotule todo controle | Use o texto de placeholder como rótulo |
| Formate valores/datas com um locale | Renderize números brutos ou strings ISO para as pessoas usuárias |

## Lista de verificação antes de abrir uma PR

- [ ] Os componentes usam exports nomeados e props totalmente tipadas
- [ ] `'use client'` fica restrito ao menor componente interativo
- [ ] O estado compartilhado usa Context somente quando justificado; não há biblioteca de estado não aprovada
- [ ] As telas assíncronas renderizam estados de carregamento, vazio e erro
- [ ] As entradas possuem rótulos, funcionam por teclado e atendem ao contraste AA
- [ ] Um teste Testing Library ao lado do componente cobre a interação (consulte [`tests.instructions.md`](tests.instructions.md))
