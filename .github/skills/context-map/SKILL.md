---
name: "context-map"
description: "Produza um mapa dos arquivos relevantes para uma tarefa, incluindo arquivos a modificar, dependências, testes relacionados, padrões de referência e riscos, antes de escrever qualquer código. Use quando a pessoa quiser delimitar o impacto, planejar alterações ou entender quais arquivos uma tarefa afeta antes da implementação."
---
# Mapa de contexto

Crie um mapa escrito de tudo o que uma tarefa afeta antes de escrever qualquer código. O mapa transforma uma alteração em aberto em um plano delimitado e revisável. Assim, quem implementa edita os arquivos corretos, atualiza as dependências certas, escreve os testes adequados e identifica os riscos antecipadamente.

> [!IMPORTANT]
> Não inicie a implementação até que o mapa de contexto esteja escrito e revisado. O mapa é o artefato produzido por esta skill. A programação só começa depois da aprovação do mapa.

## Quando usar

- "Delimite o impacto de adicionar um campo de status à API de pagamentos antes de eu programar."
- "Quais arquivos esta refatoração afeta e quais testes os cobrem?"
- "Mapeie o raio de impacto da alteração desta interface de repositório."
- "Planeje as alterações de arquivos para esta funcionalidade da Etapa 3 antes da implementação."

## Como criar o mapa

1. **Reformule a tarefa em uma frase.** Descreva o resultado observável, não o detalhe de implementação.
2. **Localize os pontos de entrada.** Encontre os arquivos responsáveis pelo comportamento, como controladores, serviços, componentes ou migrações.
3. **Rastreie as dependências diretas.** Siga as importações e exportações de cada arquivo para descobrir o que quebra se uma assinatura mudar.
4. **Encontre os testes.** Identifique os testes unitários e de integração que já cobrem o código afetado e registre onde falta cobertura.
5. **Colete padrões de referência.** Indique um arquivo existente que já resolva um problema semelhante para reproduzir sua estrutura.
6. **Avalie os riscos.** Sinalize explicitamente alterações em interfaces de programação de aplicações (APIs) públicas, migrações de banco de dados e mudanças em configurações ou segredos.

> [!NOTE]
> Nesta imersão, `backend/` e `frontend/` não existem até a Etapa 3. Portanto, o mapa de uma nova funcionalidade lista arquivos a **criar**, não apenas arquivos a modificar. `infra/` já existe. Trate tudo em `01-archaeology/legacy-sifap/` como evidência somente leitura e nunca afirme o conteúdo de um programa ou campo legado. Em vez disso, cite o critério de leitura em [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md).

## Sinais de escopo

| Sinal | Significado | Ação |
|---|---|---|
| A alteração afeta um contrato público `/api/v1` | O raio de impacto alcança todos os chamadores | Liste os chamadores e planeje uma nota de compatibilidade da API |
| A alteração modifica uma entidade JPA ou um esquema | É necessária uma migração | Adicione uma linha `db/migration` ao mapa |
| Nenhum teste cobre o código de destino | Risco de regressão | Adicione uma linha "teste a escrever" antes de programar |
| Já existe uma funcionalidade semelhante | Oportunidade de reutilização | Registre-a como padrão de referência a seguir |

## Modelo de saída

```markdown
## Mapa de contexto: adicionar um campo de status a Payment

### Arquivos a criar ou modificar
| Arquivo | Criar ou modificar | Finalidade | Alteração |
|---|---|---|---|
| backend/src/main/java/com/sifap/payment/PaymentController.java | modificar | Ponto de entrada REST | Adicionar PATCH `/api/v1/payments/{id}/status` |
| backend/src/main/java/com/sifap/payment/PaymentStatus.java | criar | Enumeração de status | Definir valores e transições permitidos |

### Dependências a verificar
| Arquivo | Relacionamento |
|---|---|
| backend/src/main/java/com/sifap/payment/PaymentService.java | Chama o mapeamento modificado do controlador |
| frontend/app/payments/page.tsx | Renderiza o status retornado pela API |

### Testes
| Teste | Status | Cobertura |
|---|---|---|
| backend/src/test/java/com/sifap/payment/PaymentControllerTest.java | existe | Estender para o novo ponto de extremidade |
| Teste de transição de PaymentStatus | a escrever | Novo comportamento da máquina de estados |

### Padrões de referência
| Arquivo | Padrão a seguir |
|---|---|
| backend/src/main/java/com/sifap/benefit/BenefitController.java | Estrutura existente de PATCH com `@Valid` |

### Riscos
- [ ] Alteração incompatível em um contrato público `/api/v1`
- [ ] Migração de banco de dados necessária
- [ ] Alteração de configuração ou segredo necessária
- [ ] O comportamento legado deve ser confirmado com as evidências somente leitura em `01-archaeology/legacy-sifap/`
```

## Critérios de qualidade

- [ ] Cada arquivo afetado pela tarefa está listado como criar ou modificar, com a alteração concreta descrita.
- [ ] As dependências diretas de cada assinatura alterada estão listadas.
- [ ] Os testes existentes estão identificados e os testes ausentes estão marcados como "a escrever".
- [ ] Pelo menos um padrão de referência está citado ou sua ausência está declarada.
- [ ] Os riscos de API pública, migração e configuração estão sinalizados antes do início da programação.
- [ ] Todo item derivado do legado cita evidências somente leitura e não afirma o conteúdo de programas legados.
