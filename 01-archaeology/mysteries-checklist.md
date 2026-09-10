# Checklist de Questões em Aberto — Estágio 1

> **Trilha:** [Kit do Time](../README.md) › [Estágio 1](README.md) › **Checklist de Questões em Aberto**

**Rastreabilidade das incertezas antes do Estágio 2.** Garante que toda questão em aberto seja registrada com evidência, hipótese marcada como não confirmada e responsável identificado.

| Campo | Valor |
|---|---|
| **Público-alvo** | Todas as duplas — preencher durante o Estágio 1 |
| **Pré-requisitos** | Ler os programas atribuídos |
| **Estágio** | Estágio 1 — Arqueologia |
| **Resultado esperado** | Lista de perguntas sem conclusão, com rastreabilidade e responsável |

> [!IMPORTANT]
> **Gate de rastreabilidade.** Uma pergunta continua em aberto até receber validação humana explícita, apoiada em evidência. Ela não pode virar resposta, regra ou requisito sem essa validação.

---

## O denominador é 20

O SIFAP, o Sistema de Fiscalização e Administração de Pagamentos, contém **20 mistérios canônicos** — regras de negócio, contradições e decisões que nunca foram documentadas e existem apenas no código. São **4 por dupla**, seguindo a escada **2 Óbvios + 1 Médio + 1 Difícil**.

| Regra | Valor |
|---|---|
| Total de mistérios canônicos na turma | **20** (`SIFAP-M-01` … `SIFAP-M-20`) |
| Por dupla | **4** |
| Dupla completa | 4 de 4 |
| Turma completa | **≥16 de 20**, sem nenhuma dupla abaixo de 2 |

> [!NOTE]
> **Por que usar um número fixo.** Sem denominador, cada dupla reportava uma quantidade diferente depois de ler exatamente o mesmo material — uma variação de mais de 30 itens dependendo da granularidade de agregação e de quantos artefatos cada pessoa abriu. O denominador **não muda**: achados fora da lista são **bônus** reconhecidos no debrief, mas não substituem um mistério canônico que ficou faltando, e os facilitadores não criam IDs canônicos durante a imersão.

Oito dos vinte são **de dois lados**: só contam com as duas evidências (código **e** DDM, ou código **e** documento legado). Comparar fontes não é opcional.

### Onde procurar — por dupla

Os rótulos indicam a **área** do mistério, nunca o achado.

| Dupla | Domínio | IDs | Programas |
|---|---|---|---|
| 1 | Cadastro | `M-01` … `M-04` | `CADBENEF`, `CADDEPEN`, `CADPROG` |
| 2 | Batch | `M-05` … `M-08` | `BATCHPGT`, `BATCHREL`, `BATCHCON` |
| 3 | Cálculo | `M-09` … `M-12` | `CALCBENF`, `CALCCORR`, `CALCDSCT`\* |
| 4 | Validação | `M-13` … `M-16` | `VALBENEF`, `VALDOCS`, `VALELEG` |
| 5 | Consultas e relatórios | `M-17` … `M-20` | `CONSBENF`, `RELPGT`, `RELAUDIT` |

\* `CALCDSCT.NSP` é leitura de apoio para a Dupla 3 — nenhum mistério canônico mora nele. Vale perguntar por que ele existe.

> [!TIP]
> **Se você ficar travado por mais de 40 minutos, peça uma dica ao facilitador.** Uma dica não custa pontos; continuar travado tira você do exercício.

---

## Para cada questão em aberto

- [ ] A pergunta foi registrada sem resposta nem conclusão.
- [ ] A evidência contém `path:line`.
- [ ] O impacto foi registrado.
- [ ] A hipótese está explicitamente marcada como **não confirmada**.
- [ ] Uma pessoa ou área responsável foi identificada.
- [ ] O status foi registrado.

---

## Estrutura do registro

| Questão em aberto | Evidência (`path:line`) | Impacto | Hipótese (não confirmada) | Pessoa/área responsável | Status |
|---|---|---|---|---|---|
| <!-- preencher --> | <!-- preencher: path:line --> | <!-- preencher --> | <!-- preencher: não confirmada --> | <!-- preencher --> | <!-- preencher: aberta / aguardando validação humana / fechada após validação humana --> |

---

## Placar da dupla

Preencha com os IDs da sua dupla (por exemplo, a Dupla 2 preenche de `M-05` a `M-08`).

| ID canônico | Encontrado | Registrado em `mysteries-found.md` |
|---|---|---|
| `SIFAP-M-__` | [ ] | [ ] |
| `SIFAP-M-__` | [ ] | [ ] |
| `SIFAP-M-__` | [ ] | [ ] |
| `SIFAP-M-__` | [ ] | [ ] |

**Achados adicionais (bônus):** <!-- liste aqui; não mudam o denominador -->

---

## Métodos para encontrar mistérios

Nenhuma destas dicas revela um achado — todas são técnicas reutilizáveis de leitura de código legado.

1. **Leia os comentários antes do código.** Em código de 29 anos, o comentário costuma ser o único lugar onde alguém tentou explicar o *porquê*. Um comentário com nome e data é ouro.
2. **Leia o cabeçalho do programa.** Linhas como `* CHANGED: yyyy-mm-dd - NAME - reason` contam a história do sistema em ordem cronológica.
3. **Compare código com documentação.** Quando `legacy-docs/` e o código discordam, você encontrou alguma coisa.
4. **Compare código com o DDM.** Tipo, tamanho e domínio de valores precisam bater entre o programa e `adabas-ddms/` — e nem sempre batem.
5. **Procure literais numéricos.** Todo número sem explicação em um cálculo levanta perguntas: de onde ele veio, quem decidiu e o que quebra se ele mudar?
6. **Pergunte "quem escreve neste campo?".** Escolha um campo do DDM e encontre todos os programas que escrevem nele. Às vezes a resposta é: nenhum.
7. **Leia o código comentado.** Blocos desativados revelam o que o sistema já fez — e por que parou.
8. **Desconfie de `ESCAPE`, de `IF` sem `ELSE` e de atribuição incondicional.** Saídas antecipadas e regras que valem sempre escondem decisões que ninguém registrou.
9. **Cruze os três programas da dupla.** Vários mistérios só aparecem quando você compara dois arquivos.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [GUIDE do Estágio 1](GUIDE.md)<br/><sub>Cronograma passo a passo.</sub> | [Registro de Questões em Aberto](mysteries-found.md)<br/><sub>Registro detalhado com evidência e responsável.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
