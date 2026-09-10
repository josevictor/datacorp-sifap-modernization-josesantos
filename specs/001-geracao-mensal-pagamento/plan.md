# Plano técnico — Geração mensal de pagamento

## Objetivo

Implementar o recorte de geração mensal de pagamento em Java 21 e Spring Boot
3.3, preservando o comportamento observável dos requisitos `REQ-001` a
`REQ-009`. A implementação deve ser modular, manter valores monetários com
precisão decimal, impedir duplicidade por CPF e período e executar por Docker
em todas as etapas de desenvolvimento, teste e demonstração.

## Limites do módulo

- **Entrada:** solicitação de geração para CPF, programa e período.
- **Domínio:** validação de período, elegibilidade cadastral mínima, cálculo do
  bruto, adicional de dezembro, abono, líquido e decisão de duplicidade.
- **Persistência:** beneficiário, programa e pagamento.
- **Saída:** pagamento gerado ou rejeição/ignorado com motivo observável.
- **Não incluído:** decisão sobre `CALCDSCT`, região `99`, proporcionalidade do
  décimo-terceiro e correção IPCA.
- **Execução:** nenhum comando de build, teste ou banco deve depender de Maven,
  Java ou PostgreSQL instalados no host; a execução local deve ocorrer por
  Docker/Compose.

## Componentes planejados

1. **Serviço de aplicação de geração:** coordena validação, consulta de
   duplicidade, cálculo e persistência.
2. **Serviço de cálculo:** concentra a fórmula de `CALCBENF`, incluindo
   truncamento monetário.
3. **Portas de repositório:** isolam consultas de beneficiário, programa e
   pagamento.
4. **Modelo de pagamento:** representa valores, período, tipo e situação do
   pagamento.
5. **Adaptador de entrada:** expõe o caso de uso por
   `POST /api/v1/payments/monthly-generations`.
6. **Empacotamento Docker:** fornece imagem do backend, PostgreSQL 16 em
   contêiner, rede Compose e comandos reproduzíveis para testes e execução.

## Dados e invariantes

- Valores monetários devem usar `BigDecimal` com escala controlada; não usar
  `double` ou `float`.
- O período deve representar `YYYYMM` e ter mês entre 01 e 12.
- A combinação CPF + período deve ser única no pagamento.
- Pagamento concluído deve ter situação `G`.
- Resultados monetários devem ser truncados para duas casas, não arredondados.
- O CPF não deve aparecer sem máscara em logs.
- Segredos e senhas de desenvolvimento devem vir de `.env` ignorado pelo Git;
  valores reais nunca devem ser versionados.

## Estratégia de testes

- Testes unitários para cada requisito de cálculo e truncamento.
- Testes unitários para estados de beneficiário e validação de período/CPF.
- Teste de integração de persistência para a restrição CPF + período, usando o
  PostgreSQL 16 do Compose.
- Teste de integração do caso de uso para confirmar criação de pagamento com
  situação `G`.
- Cada teste deve citar o `REQ-ID` correspondente em comentário inline.
- Os testes de integração devem usar PostgreSQL 16 em contêiner; não usar H2.
- A validação local da feature deve oferecer um comando Docker/Compose único
  para executar build e testes.

## Estratégia Docker

- Criar `backend/Dockerfile` com build reproduzível da aplicação Java 21.
- Criar Compose de desenvolvimento com serviços `backend` e `db`.
- Criar um serviço ou perfil de testes no Compose para executar os testes do
  backend contra o PostgreSQL 16 do Compose, sem exigir Maven ou Java no host.
- Usar PostgreSQL 16 em contêiner para desenvolvimento e integração.
- Ler credenciais somente de `.env` local ignorado pelo Git ou de variáveis de
  ambiente da execução.
- Documentar os comandos Docker no README do backend quando a estrutura for
  criada.

## Riscos e decisões pendentes

| Risco | Mitigação |
|---|---|
| `CALCBENF` e `CALCDSCT` representam regras de desconto diferentes | Manter `CALCDSCT` fora deste recorte e exigir validação humana antes de ampliá-lo. |
| Fórmula de dezembro não usa meses ativos apesar de comentário histórico | Preservar somente o código observado e manter `SIFAP-M-11` aberto. |
| Região `99` não possui regra confirmada | Não criar regra moderna específica; manter o item fora do escopo. |
| Batch legado repete a fórmula após `CALLNAT` | Não alterar o legado; cobrir o comportamento escolhido por testes e registrar `SIFAP-M-10`. |
| Ambiente local divergente entre pessoas do time | Executar build, testes, backend e banco via Docker/Compose. |

## Ordem de implementação

1. Criar modelo e objetos de valor monetários/período.
2. Escrever testes unitários de validação e cálculo.
3. Implementar cálculo e regras de dezembro.
4. Escrever teste de integração da unicidade CPF + período.
5. Implementar persistência e serviço de aplicação.
6. Adicionar adaptador de entrada e testes de contrato.
7. Criar Dockerfile e Compose para execução local e testes.
8. Executar análise de rastreabilidade dos `REQ-ID`.
