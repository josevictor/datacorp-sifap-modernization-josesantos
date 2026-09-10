---
description: "Use ao projetar ou revisar arquitetura de Monólito Modular, limites de pacotes por funcionalidade, mapeamento JPA e migração Strangler Fig."
applyTo: "backend/src/main/java/**,backend/pom.xml,backend/build.gradle*"
---

# Guia de arquitetura de Monólito Modular

Este arquivo é ativado quando você trabalha em código-fonte Java ou configurações de build do backend. Ele ensina a arquitetura-alvo: um **Monólito Modular**, não microsserviços, com limites de pacotes por funcionalidade, contextos delimitados, mapeamento de FDT Adabas para JPA, convenções arquiteturais do Spring Boot 3.3 e formato de migração Strangler Fig. Ele **não** define detalhes de controller, DTO, validação ou resposta de erro, que pertencem a [`backend.instructions.md`](backend.instructions.md); segurança pertence a [`security.instructions.md`](security.instructions.md); migrações de schema pertencem a [`database.instructions.md`](database.instructions.md); e leitura de código legado pertence a [`natural-adabas.instructions.md`](natural-adabas.instructions.md).

## Princípio fundamental: um implantável, vários módulos

O sistema-alvo é uma única aplicação Spring Boot com limites internos claros entre módulos. Cada contexto delimitado é um módulo Maven (ou pacote de nível superior) responsável por suas camadas de domínio, repositório e serviço.

Por que usar um Monólito Modular em vez de microsserviços:

- **Restrição da imersão**: 8 horas não bastam para gerenciar sistemas distribuídos, descoberta de serviços e comunicação entre serviços.
- **Orçamento de complexidade**: um monólito com limites fortes entre módulos oferece 80% dos benefícios dos microsserviços (autonomia da equipe e responsabilidade clara) com 20% do custo operacional.
- **Caminho de migração**: um Monólito Modular bem estruturado pode ser decomposto em microsserviços depois, se necessário. O caminho inverso é muito mais difícil.

## Estrutura de pacotes por funcionalidade

Organize o código por capacidade de negócio, não por camada técnica:

```
src/main/java/com/example/app/
├── <feature>/                  # Contexto delimitado definido pela equipe
│   ├── <Feature>Controller.java
│   ├── <Feature>Service.java
│   ├── <Feature>Repository.java
│   ├── <Feature>.java
│   └── <Feature>Dto.java
├── shared/                     # Kernel compartilhado
│   ├── audit/                  # Transversal: trilha de auditoria
│   └── exception/              # Transversal: tratamento de erros
└── Application.java            # Ponto de entrada do Spring Boot
```

Regras:

- Um módulo **NUNCA** DEVE importar diretamente classes internas de outro módulo. Use interfaces ou eventos.
- O pacote `shared/` contém somente responsabilidades transversais (auditoria, exceções e entidades base).
- Cada módulo possui seus próprios `*Repository`, `*Service` e `*Controller`.

## Limites dos contextos delimitados

Ao decidir onde traçar limites entre módulos, pergunte:

1. **Quem é responsável por estes dados?** Se duas funcionalidades compartilham a mesma tabela, podem pertencer ao mesmo contexto.
2. **O que muda em conjunto?** Funcionalidades modificadas no mesmo sprint pertencem juntas.
3. **O que pode falhar de forma independente?** Se a falha da Funcionalidade A NÃO DEVE quebrar a Funcionalidade B, elas pertencem a contextos distintos.

Um padrão comum na modernização de legado Natural/Adabas é cada arquivo Adabas (FNR) corresponder a um contexto delimitado, embora alguns arquivos contenham dados de referência compartilhados pertencentes a um kernel compartilhado.

## Mapeamento JPA a partir de FDT Adabas

### Campos simples

| Formato Adabas | Tipo Java | Anotação JPA |
|---|---|---|
| `A` (alphanumeric) | `String` | `@Column(length = N)` |
| `N` (numeric, no decimal) | `Long` or `Integer` | `@Column` |
| `N` (numeric, with decimal) | `BigDecimal` | `@Column(precision = P, scale = S)` |
| `P` (packed decimal) | `BigDecimal` | `@Column(precision = P, scale = S)` |
| `D` (date) | `LocalDate` | `@Column` |
| `T` (time/datetime) | `LocalDateTime` | `@Column` |
| `B` (binary) | `byte[]` | `@Column` / `@Lob` |

### Campos MU (múltiplos valores) → JSONB

```java
@Column(columnDefinition = "jsonb")
@JdbcTypeCode(SqlTypes.JSON)
private List<String> alternateNames;  // Era um campo MU no Adabas
```

Ou use `@ElementCollection` quando houver necessidade de consulta:

```java
@ElementCollection
@CollectionTable(name = "person_alternate_names")
private List<String> alternateNames;
```

### PE (grupos periódicos) → @OneToMany

```java
@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
@JoinColumn(name = "person_id")
private List<AddressHistory> addressHistory;  // Era um grupo PE
```

Nesse caso, `AddressHistory` é uma `@Entity` com tabela própria.

## Convenções do Spring Boot 3.3

- **Injeção por construtor**: sem `@Autowired` em campo. Use `@RequiredArgsConstructor` (Lombok) ou construtores explícitos.
- **Records para DTOs**: `public record ResourceDto(Long id, String label) {}`
- **Validação na camada de controller**: `@Valid @RequestBody ResourceDto dto` com anotações Bean Validation no DTO.
- **@Transactional somente na camada de serviço**: NUNCA em repositórios, NUNCA em controllers.
- **Optional para retornos anuláveis**: `Optional<Resource> findById(Long id)`; NUNCA retorne `null` de métodos públicos.
- **Interfaces sealed para uniões de tipos**: `sealed interface ResourceState permits StateA, StateB {}`

## Padrão de tratamento de erros

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ProblemDetail> handleNotFound(EntityNotFoundException ex) {
        ProblemDetail detail = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(detail);
    }
}
```

Use `ProblemDetail` (RFC 7807) em todas as respostas de erro.

## Padrão Strangler Fig

Quando o sistema moderno precisar coexistir com o sistema legado:

1. **Fachada**: todas as solicitações passam por uma camada de roteamento
2. **Caminho novo**: funcionalidades novas ou migradas são tratadas pelos módulos Spring Boot
3. **Caminho legado**: funcionalidades não migradas são encaminhadas ao sistema legado
4. **Migração gradual**: conforme cada funcionalidade é migrada, sua rota muda do legado para o moderno

Esse padrão se aplica até dentro do escopo da imersão: as equipes podem não migrar tudo, e isso é aceitável. A arquitetura DEVE oferecer suporte adequado à migração parcial.

## Convenções

| Regra | Justificativa |
|---|---|
| Um implantável Spring Boot com vários módulos internos | Preserva a velocidade de entrega da imersão e mantém limites explícitos |
| Pacotes por capacidade de negócio | Módulos correspondem a contextos delimitados, não a camadas técnicas |
| Internos privados; acesso entre módulos por interfaces ou eventos | Impede acoplamento oculto entre contextos |
| Tipos FDT Adabas mapeados deliberadamente para Java/JPA | Evita truncamento silencioso, perda de precisão e relacionamentos incorretos |
| `@Transactional` somente em serviços e injeção por construtor | Mantém explícitos os limites de persistência e as dependências |
| `ProblemDetail` para erros | Oferece a todos os módulos um formato de erro legível por máquina |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Mantenha uma aplicação Spring Boot com módulos internos claros | Crie aplicações Spring Boot ou microsserviços separados para cada contexto |
| Coloque a lógica de negócio em serviços Java | Mova a lógica para stored procedures ou funções PostgreSQL |
| Use JPA/JPQL ou consultas derivadas do Spring Data | Concatene strings para criar SQL |
| Use injeção por construtor | Use injeção em campo com `@Autowired` |
| Retorne `Optional` quando o resultado puder estar ausente | Retorne `null` de métodos públicos |
| Ofereça suporte à migração parcial com uma fachada Strangler Fig | Presuma que todo o sistema legado será migrado de uma vez |

## Lista de verificação antes de abrir uma PR

- [ ] O código novo fica em um implantável Spring Boot e é organizado por capacidade de negócio
- [ ] Nenhum módulo importa diretamente classes internas de outro; interfaces ou eventos definem o limite
- [ ] Repositórios, serviços, controllers, entidades e DTOs ficam no módulo responsável ou no kernel compartilhado
- [ ] Os campos FDT Adabas foram mapeados para tipos Java/JPA preservando precisão e semântica de MU, PE e descritores
- [ ] `@Transactional` aparece somente em serviços, as dependências usam injeção por construtor e métodos públicos não retornam `null`
- [ ] O projeto pode coexistir com caminhos legados não migrados pelo roteamento Strangler Fig
