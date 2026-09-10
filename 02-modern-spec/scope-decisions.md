# Decisões de escopo — Estágio 2

> **Trilha:** [Kit do Time](../README.md) › [Estágio 2](README.md) › **Decisões de escopo**

**Registre as decisões de escopo tomadas durante o Estágio 2: o que foi selecionado, o que foi adiado e quais questões permanecem em aberto.**

| Campo | Valor |
|---|---|
| **Público-alvo** | Dupla 2 durante o Estágio 2; Duplas 3 e 4 durante o handoff H2 |
| **Finalidade** | Apoiar a conversa do estágio; não substitui os artefatos formais do Spec-Kit |
| **Feature relacionada** | `specs/<NNN>-<feature>/` |

> [!NOTE]
> Os entregáveis formais permanecem em `specs/<NNN>-<feature>/spec.md`, `plan.md` e `tasks.md`. Não registre requisitos EARS completos aqui. Este arquivo registra somente decisões de escopo e questões em aberto.

---

## Decisões de escopo

| Decisão | Evidência ou justificativa | Impacto nos artefatos formais |
|---|---|---|
| Selecionar geração mensal de pagamento como primeira feature moderna. | `BATCHPGT.NSP`, `CALCBENF.NSN`, `PAYMENT.ddm`, `SOCPROG.ddm`; regras catalogadas em `01-archaeology/business-rules-catalog.md`. | `specs/001-geracao-mensal-pagamento/spec.md` |
| Preservar o comportamento do cálculo atualmente conectado ao fluxo do batch. | `CALCBENF.NSN` e `BATCHPGT.NSP`; a divergência com `CALCDSCT.NSP` permanece aberta em `SIFAP-M-09`. | `specs/001-geracao-mensal-pagamento/plan.md` |
| Adiar correção IPCA, regras detalhadas de desconto, região `99` e proporcionalidade do décimo-terceiro. | `01-archaeology/mysteries-found.md`, itens `SIFAP-M-09` a `SIFAP-M-12`. | Não entram nos requisitos desta feature. |
| Executar desenvolvimento, testes e demonstração da feature por Docker. | Decisão operacional da equipe nesta sessão; instruções de infraestrutura exigem Compose com segredos via `.env` e PostgreSQL em contêiner. | `specs/001-geracao-mensal-pagamento/plan.md` e `tasks.md` incluem gate Docker-first. |
| Para a feature `001-geracao-mensal-pagamento`, usar a dedução simplificada efetivamente conectada ao fluxo de geração mensal. | `BATCHPGT.NSP:412-418` recalcula e persiste o pagamento com desconto simplificado; `CALCBENF.NSN:347-357` contém a mesma regra; `CALCDSCT.NSP` não é chamado no trecho executado da geração mensal analisada. | A implementação atual mantém a dedução simplificada. `CALCDSCT` deve virar feature separada de descontos detalhados. |
| No sistema moderno, não duplicar a fórmula do batch; centralizar cálculo em um serviço único. | `BATCHPGT.NSP:330-425` chama `CALCBENF` e depois mantém cálculo inline ativo por pendência histórica; duplicar isso em Java criaria divergência deliberada. | `PaymentCalculationService` é a fonte única de cálculo na implementação moderna. |
| Para a feature atual, preservar o código observado do décimo-terceiro sem proporcionalidade por meses ativos. | `CALCBENF.NSN:280-292` calcula o adicional de dezembro sem variável de meses ativos; o documento de 2012 declara o tema como pendente/incompleto. | A proporcionalidade permanece fora da feature e requer decisão de negócio futura. |
| Para a feature atual, tratar regiões fora de 1 a 25, incluindo `99`, com fator neutro `1.0000`. | `CALCBENF.NSN:218-231` aplica a tabela somente para 1 a 25 e usa `1.0000` nos demais casos; `LDASIFAP.NSL:38-48` marca `99` como especial sem explicar regra própria. | A implementação preserva o comportamento observado, sem atribuir significado de negócio ao código `99`. |
| Selecionar validação de elegibilidade como terceira feature. | `BATCHPGT.NSP:369-379` chama `VALELEG` por `CALLNAT` antes do cálculo e ignora o beneficiário quando o retorno é diferente de zero; a feature `001` gera pagamento sem essa validação. | `specs/003-elegibilidade/spec.md` |
| Preservar o desvio da região `99` em `VALELEG`, que dispensa todas as validações seguintes. | `VALELEG.NSN:120-128` encerra a rotina como elegível; nenhuma regra de negócio localizada autoriza o desvio. | `REQ-023` preserva o comportamento e isola o desvio em método próprio para reversão barata. Questão `SIFAP-M-12`. |
| Não implementar as regras de elegibilidade descritas na documentação de 2012 e ausentes do código. | `BUSINESS-RULES-2012.md:186-196` cita dados bancários, limite de dois programas, atualização em 24 meses e auditoria bloqueante; nenhuma existe em `VALELEG.NSN:120-262`. O mesmo documento já se mostrou incorreto em `SIFAP-M-09`. | Registrado em `specs/003-elegibilidade/tasks.md` como regras não implementadas por ausência de evidência. |
| Não replicar a divergência de cálculo de idade entre `BATCHPGT` e `VALELEG`. | `BATCHPGT.NSP:336-348` aplica a janela de século antes de calcular a idade; `VALELEG.NSN:75-96` descarta o parâmetro recebido e recalcula sem a janela. A divergência decorre de contrato de PDA não revisto, não de regra de negócio. | `specs/003-elegibilidade/plan.md` usa fonte única de idade; divergência registrada como achado `BONUS`. |

---

## Questões em aberto

| Questão | Fonte consultada | Próxima pessoa responsável |
|---|---|---|
| Para futuras features, `CALCDSCT` substitui ou complementa a dedução simplificada do fluxo mensal? | `mysteries-found.md#SIFAP-M-09` | Coordenação de benefícios + operação do batch |
| A proporcionalidade do décimo-terceiro deve ser criada como regra nova ou descartada formalmente? | `mysteries-found.md#SIFAP-M-11` | Coordenação de benefícios |
| A região `99` possui significado operacional além do fator neutro observado no cálculo? **Evidência técnica encontrada:** em `VALELEG` ela dispensa todas as validações de elegibilidade. A decisão de negócio continua aberta. | `mysteries-found.md#SIFAP-M-12`; `VALELEG.NSN:120-128` | Coordenação de benefícios + DBA + auditoria |
| As regras de elegibilidade descritas na documentação de 2012 e ausentes do código foram removidas, nunca implementadas ou vivem em outro programa? | `mysteries-found.md`, achado `BONUS`; `BUSINESS-RULES-2012.md:186-196` | Coordenação de benefícios + arquitetura |
| Quantos beneficiários ativos recebem hoje por programa cujo tipo os recusaria, e o que fazer com eles? As regras por tipo de programa são literais fixos no legado e não podem ser desativadas por parâmetro, ao contrário de faixa etária, teto de renda e NIS. Na primeira execução com a validação ativa, esses beneficiários deixam de receber. | `VALELEG.NSN:196-243`; `specs/003-elegibilidade/plan.md`, seção sobre padrões inertes | Coordenação de benefícios + DBA + operação do batch |

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Guia do Estágio 2](GUIDE.md)<br/><sub>Especificação moderna passo a passo.</sub> | [Template de ADR](ADR-TEMPLATE.md)<br/><sub>Registre a decisão de escopo como uma ADR.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
