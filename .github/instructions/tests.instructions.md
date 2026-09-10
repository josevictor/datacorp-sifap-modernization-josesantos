---
description: "Use ao criar ou revisar testes automatizados, estratégia de testes, specs, lacunas de cobertura, testes de regressão e portões de qualidade."
applyTo: "**/*.test.*,**/*.spec.*,**/tests/**"
---

# Convenções de testes — JUnit, Vitest e rastreabilidade

Este arquivo é ativado em qualquer arquivo de teste (`*.test.*`, `*.spec.*` ou qualquer arquivo em um path `tests/`), tanto no backend quanto no frontend. Ele ensina estrutura e nomenclatura de testes, ferramentas de backend (JUnit 5 + Testcontainers) e frontend (Vitest + Testing Library), rastreabilidade de REQ-ID e metas de cobertura. Os testes são escritos **durante** a implementação, nunca adicionados depois.

## Pirâmide de testes

| Camada | Ferramentas | Proporção |
|---|---|---|
| Unidade (serviços, lógica pura) | JUnit 5 / Vitest, sem E/S | Maioria dos testes |
| Integração (repositórios, componentes) | Testcontainers / Testing Library | Menos |
| Ponta a ponta | Somente o fluxo crítico | Menor quantidade |

A skill [`test-strategy`](../skills/test-strategy/SKILL.md) detém as decisões sobre o formato da pirâmide e as metas de cobertura.

## Estrutura: Preparar-Agir-Verificar

Cada teste possui três fases visíveis e verifica um comportamento. Simule somente limites externos, nunca o banco de dados nem a classe em teste.

```java
@Test
void should_reject_duplicate_label() { // REQ-021
    resourceRepository.save(Resource.of("alpha", new BigDecimal("10.00"))); // Preparar
    var request = new CreateResourceRequest("alpha", new BigDecimal("5.00"));
    assertThatThrownBy(() -> resourceService.create(request))            // Agir
        .isInstanceOf(ResourceConflictException.class);                  // Verificar
}
```

## Nomenclatura

Nomeie testes como `should_<expected behavior>_when_<condition>` (backend) ou expresse a mesma intenção em `it(...)` da Testing Library (frontend).

```text
should_return_409_when_identifier_already_exists
should_render_empty_state_when_no_resources
```

## Backend: JUnit 5 + Testcontainers

Os testes de repositório e integração executam com PostgreSQL 16 real em contêiner, nunca H2, para que o comportamento corresponda à produção. Vincule o contêiner com `@ServiceConnection`.

```java
@Testcontainers
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class ResourceRepositoryTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Autowired
    ResourceRepository resourceRepository;

    @Test
    void should_find_resource_by_label_when_it_exists() { // REQ-021
        resourceRepository.save(Resource.of("alpha", new BigDecimal("10.00")));
        assertThat(resourceRepository.findByLabel("alpha")).isPresent();
    }
}
```

A lógica de negócio do backend deve incluir fluxo de sucesso, falha de validação e falha de autenticação.

## Frontend: Vitest + Testing Library

Consulte por papel ou rótulo acessível, nunca por test-id quando existir um papel, e conduza a interação com `user-event`. Evite testes somente de snapshot.

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { ArchiveButton } from './ArchiveButton';

describe('ArchiveButton', () => {
  it('should call onArchive when clicked', async () => { // REQ-032
    const onArchive = vi.fn().mockResolvedValue(undefined);
    render(<ArchiveButton id="1" onArchive={onArchive} />);
    await userEvent.click(screen.getByRole('button', { name: /archive/i }));
    expect(onArchive).toHaveBeenCalledWith('1');
  });
});
```

## Rastreabilidade de REQ-ID

Todo teste que verifica um requisito nomeia seu REQ-ID em um comentário inline. Isso alimenta o relatório não bloqueante `spec-traceability` (consulte [`requirements.instructions.md`](requirements.instructions.md)), que lista REQ-IDs ainda não referenciados por testes.

## Metas de cobertura

O mínimo do repositório é **≥ 80% de linhas** e **≥ 70% de branches**; classes de serviço e lógica de negócio devem buscar valor maior (cerca de 85% de linhas). A CI executa Jacoco (backend) e Vitest `--coverage` (frontend) e informa os números. Configure os limites em `pom.xml` e na configuração do Vitest para que `verify`/`test` falhem abaixo do mínimo.

> [!NOTE]
> Cobertura é um mínimo, não uma meta. Uma branch sem asserção não foi testada mesmo quando a linha está "coberta"; verifique o comportamento, não somente a chamada.

## Convenções

| Regra | Justificativa |
|---|---|
| Preparar-Agir-Verificar, um comportamento por teste | Legível e isola a falha |
| Simule somente limites externos | Banco real via Testcontainers detecta bugs reais |
| Nomenclatura `should_<behavior>_when_<condition>` | A intenção fica clara no relatório |
| `// REQ-NNN` inline em testes de requisitos | Mantém ativa a rastreabilidade entre spec e teste |
| Escritos durante a implementação | Código sem testes não é integrado |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Use Testcontainers PostgreSQL 16 | Substitua por H2 nos testes de integração |
| Consulte por papel/rótulo | Consulte por `data-testid` quando existir um papel |
| Verifique comportamento e branches de borda | Dependa somente de snapshots ou cobertura de linhas |
| Escreva o teste junto com o código | Adicione testes depois que a funcionalidade estiver "pronta" |

## Lista de verificação antes de abrir uma PR

- [ ] O comportamento novo possui testes unitários; a persistência possui teste de integração com Testcontainers
- [ ] Os testes seguem Preparar-Agir-Verificar e a nomenclatura `should_..._when_...`
- [ ] Os testes orientados por requisitos possuem comentário inline `// REQ-NNN`
- [ ] A lógica de negócio cobre fluxo de sucesso, falha de validação e falha de autenticação
- [ ] A cobertura atende ao mínimo de ≥ 80% de linhas / ≥ 70% de branches
- [ ] Nenhum limite externo fica sem simulação e nenhuma dependência real necessária é simulada
