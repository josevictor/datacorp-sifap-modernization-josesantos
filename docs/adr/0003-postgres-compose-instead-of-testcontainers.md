# ADR-0003: Usar PostgreSQL do Compose em vez de Testcontainers

> **Trilha:** [Kit do Time](../../README.md) › [Documentação](../README.md) › [ADRs](README.md) › **ADR-0003**

| Campo | Valor |
|---|---|
| **Status** | accepted |
| **Data** | 2026-09-10 |
| **Autores** | Pessoa Desenvolvedora — José Santos |
| **Substitui** | N/A |

---

## Contexto

[`tests.instructions.md`](../../.github/instructions/tests.instructions.md)
prescreve Testcontainers com `@ServiceConnection` para testes de integração, e
o `pom.xml` do backend inclui as dependências correspondentes.

O kit exige que build, testes e execução ocorram por Docker, sem Java, Maven ou
PostgreSQL instalados no host. Isso coloca o Maven dentro de um contêiner
(`backend-test`), e o Testcontainers passa a precisar de acesso ao daemon
Docker do host a partir de dentro de outro contêiner.

Duas tentativas falharam no ambiente de desenvolvimento:

1. Montar `/var/run/docker.sock` no contêiner de testes produziu
   `client version 1.32 is too old. Minimum supported API version is 1.40`.
2. Fixar `DOCKER_API_VERSION: "1.40"` não alterou o resultado.

A causa é a versão do cliente Docker embutida na imagem
`maven:3.9.9-eclipse-temurin-21`, que não acompanha o daemon do host. Resolver
exigiria fixar imagem, versão de cliente e versão de daemon simultaneamente —
um acoplamento frágil entre o repositório e a máquina de cada pessoa do time.

---

## Decisão

Os testes de integração usarão um serviço PostgreSQL 16 dedicado do Docker
Compose, chamado `db-test`, em vez de contêineres gerenciados pelo
Testcontainers.

O serviço usa `tmpfs` para o diretório de dados, de modo que cada execução da
suíte começa com um banco limpo e nada persiste entre execuções. As classes de
teste recebem a conexão por `SPRING_DATASOURCE_*` e usam
`@AutoConfigureTestDatabase(replace = NONE)`.

A intenção original da instrução é preservada: os testes continuam rodando
contra PostgreSQL 16 real, com migrações Flyway aplicadas, e o H2 permanece
proibido.

---

## Alternativas consideradas

| Alternativa | Por que foi rejeitada |
|---|---|
| Testcontainers com socket Docker montado | Falhou por incompatibilidade entre o cliente Docker da imagem Maven e o daemon do host; a correção acopla o repositório à versão do daemon de cada máquina. |
| Testcontainers com Docker-in-Docker privilegiado | Exige contêiner privilegiado, ampliando a superfície de risco e a complexidade de configuração para um ganho que o serviço `db-test` já entrega. |
| Executar Maven no host | Viola a exigência de execução integralmente por Docker e reintroduz divergência de ambiente entre as pessoas do time. |
| Usar H2 nos testes de integração | Proibido pelas instruções do kit; não reproduz o comportamento do PostgreSQL em tipos numéricos, o que é crítico para o truncamento monetário do SIFAP. |

---

## Consequências

- **Mais fácil:** a suíte roda com um único comando
  (`docker compose --profile test run --rm backend-test`) em qualquer máquina
  com Docker, sem depender da versão do daemon.
- **Mais fácil:** o banco de testes é isolado do banco de desenvolvimento,
  eliminando falhas causadas por dados de demonstração ou registros criados
  manualmente.
- **Mais difícil:** o ciclo de vida do banco passa a ser responsabilidade do
  Compose, não do código de teste; quem escreve testes precisa conhecer o
  perfil `test`.
- **Riscos:** as dependências do Testcontainers permanecem no `pom.xml` sem
  uso, o que pode induzir alguém a reintroduzir a abordagem que falhou.
- **Riscos:** a suíte não cria bancos por classe de teste, então testes que
  dependam de estado precisam de `@Transactional` para isolamento.
- **Mitigações:** este ADR é citado no README do backend; as classes de teste
  usam `@Transactional`; o `tmpfs` garante base limpa a cada execução.

---

## Relacionados

- REQ-IDs: `REQ-002`, `REQ-003`, `REQ-004`, `REQ-009`, `REQ-019`
- ADRs: N/A
- Instruções: [`tests.instructions.md`](../../.github/instructions/tests.instructions.md)
- Arquivos: [`compose.yaml`](../../compose.yaml), [`backend/README.md`](../../backend/README.md)

---

## Referências

- Documentação do Docker Compose sobre perfis de serviço e `tmpfs`.
- Registro de execução da suíte em
  [`specs/001-geracao-mensal-pagamento/tasks.md`](../../specs/001-geracao-mensal-pagamento/tasks.md).

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [ADR-0002](0002-trilingual-documentation-portal.md)<br/><sub>Portal de documentação trilíngue.</sub> | [ADRs — Índice](README.md)<br/><sub>Índice das decisões registradas.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
