# Arquitetura

## Seções principais (obrigatórias)

### 1) Estilo arquitetural

- Estilo principal: [camadas/funcionalidades/orientado a eventos/outro]
- Motivo da classificação: [justificativa breve baseada em evidências]
- Restrições principais: [duas ou três restrições que moldam o design]

### 2) Fluxo do sistema

```text
[entrada] -> [processamento] -> [lógica de domínio] -> [dados/integração] -> [resposta/saída]
```

Descreva o fluxo em quatro a seis etapas usando evidências baseadas em arquivos.

### 3) Responsabilidades de camadas e módulos

| Camada ou módulo | Responsável por | Não deve conter | Evidência |
|-----------------|------|--------------|----------|
| [nome] | [responsabilidade] | [não responsabilidade] | [arquivo] |

### 4) Padrões reutilizados

| Padrão | Onde foi encontrado | Por que existe |
|---------|-------------|---------------|
| [instância única/repositório/adaptador/etc.] | [caminho] | [motivo] |

### 5) Riscos arquiteturais conhecidos

- [Risco 1 + impacto]
- [Risco 2 + impacto]

### 6) Evidências

- [path/to/entrypoint]
- [path/to/main-layer-files]
- [path/to/data-or-integration-layer]

## Seções ampliadas (opcionais)

Adicione somente quando necessário:

- Detalhes da ordem de inicialização
- Diagramas de topologia assíncrona ou de eventos
- Catálogo de antipadrões com caminhos de refatoração
- Análise de modos de falha e postura de resiliência
