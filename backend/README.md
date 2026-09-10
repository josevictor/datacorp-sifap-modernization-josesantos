# SIFAP backend

Backend Spring Boot 3.3 em Java 21 para o recorte de geração mensal de
pagamento descrito em `../specs/001-geracao-mensal-pagamento/`.

## Executar com Docker

Copie as variáveis de exemplo e ajuste a senha local:

```bash
cp ../.env.example ../.env
docker compose up --build
```

Se a porta `5432` ou `8080` já estiver ocupada no host, ajuste no `.env`:

```dotenv
POSTGRES_HOST_PORT=5433
BACKEND_HOST_PORT=8081
```

Isso muda apenas a porta publicada no host. A comunicação entre os
contêineres continua em `db:5432`.

A API estará disponível em:

- `http://localhost:8080/actuator/health`
- `http://localhost:8080/swagger-ui/index.html`

Exemplo de geração com os dados de demonstração carregados pelo Compose:

```bash
curl -X POST http://localhost:8080/api/v1/payments/monthly-generations \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"52998224725","period":202609}'
```

Recálculo de descontos de um pagamento existente, equivalente ao programa
`CALCDSCT.NSP`. O pagamento de demonstração já vem com descontos registrados:

```bash
curl -X POST \
  http://localhost:8080/api/v1/payments/00000000-0000-0000-0000-000000000201/discount-calculations
```

O total resultante é `300,00`: a soma dos descontos chega a `310,00` e é
limitada ao teto de 30% do valor bruto.

## Rodar testes com Docker

```bash
docker compose --profile test run --rm backend-test
```

Os testes rodam contra o serviço `db-test`, um PostgreSQL 16 dedicado e
efêmero (`tmpfs`), isolado do banco de desenvolvimento. Isso evita que dados
de demonstração ou pagamentos criados manualmente interfiram nas contagens
verificadas pelos testes. Não use H2.

A escolha por não usar Testcontainers está registrada no
[ADR-0003](../docs/adr/0003-postgres-compose-instead-of-testcontainers.md).

Para descartar o banco de testes ao final:

```bash
docker compose --profile test down
```
