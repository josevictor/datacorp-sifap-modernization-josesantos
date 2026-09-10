# Padrões de teste

## Seções principais (obrigatórias)

### 1) Stack e comandos de teste

- Estrutura de teste principal: [NOME + VERSÃO]
- Ferramentas de asserção/simulação: [FERRAMENTAS]
- Comandos:

```bash
[executar todos os testes]
[executar testes unitários]
[executar testes de integração/e2e]
[executar cobertura]
```

### 2) Estrutura dos testes

- Padrão de localização dos arquivos de teste: [junto ao código/pasta de testes/etc.]
- Convenção de nomes: [padrão]
- Arquivos de configuração e onde são executados: [caminhos]

### 3) Matriz de escopo dos testes

| Escopo | Coberto? | Alvo típico | Notas |
|-------|----------|----------------|-------|
| Unitário | [sim/não] | [módulos/serviços] | [notas] |
| Integração | [sim/não] | [limites de API/dados] | [notas] |
| Ponta a ponta (E2E) | [sim/não] | [fluxos de usuário] | [notas] |

### 4) Estratégia de simulações e isolamento

- Abordagem principal de simulações: [módulo/classe/rede]
- Garantias de isolamento: [o que é redefinido e quando]
- Modo de falha comum nos testes: [nota breve]

### 5) Sinais de cobertura e qualidade

- Ferramenta de cobertura + limite: [valor ou TODO]
- Cobertura atual informada: [valor ou TODO]
- Lacunas conhecidas/áreas instáveis: [lista]

### 6) Evidências

- [path/to/test-config]
- [path/to/representative-test-file]
- [path/to/ci-or-coverage-config]

## Seções ampliadas (opcionais)

Adicione somente quando necessário:

- Padrões de suítes específicos da estrutura de software
- Receitas detalhadas de simulações por tipo de dependência
- Catálogo histórico de testes instáveis
- Gargalos de desempenho dos testes e ideias de otimização
