# Catálogo de Regras de Negócio — SIFAP Legado

> **Trilha:** [Kit do Time](../README.md) › [Estágio 1](README.md) › **Catálogo de Regras de Negócio**

**Artefato preenchido pelo time durante o Estágio 1.** Cada dupla extrai as regras dos programas `.NSP` e `.NSN` que recebeu e as registra aqui, com rastreabilidade obrigatória até o programa de origem.

| Campo | Valor |
|---|---|
| **Público-alvo** | Todas as duplas — cada dupla preenche a seção dos seus programas |
| **Pré-requisitos** | Ler os programas `.NSP` e `.NSN` atribuídos |
| **Estágio** | Estágio 1 — Arqueologia |
| **Resultado esperado** | Catálogo com `Programa de origem` preenchido para cada regra candidata |

> [!NOTE]
> Cada regra cita o programa de origem com um intervalo de linhas (`arquivo.NSP:Linicio-Lfim` ou `arquivo.NSN:Linicio-Lfim`) e é classificada como **Confirmada** (corroborada pela documentação histórica em `legacy-sifap/legacy-docs/`), **Inferida** (só a partir do código) ou **Mistério** (questão em aberto — registre-a também em [`mysteries-found.md`](mysteries-found.md) com evidência `path:line`, hipótese não confirmada, responsável e status).

> [!IMPORTANT]
> Guia passo a passo: [`GUIDE.md`](GUIDE.md).

**Time**: Investigação assistida — recorte de cálculo, descontos, correção e geração de pagamentos.

---

## Regras de `CALCBENF.NSN`

| # | Enunciado da regra | Candidato EARS | Origem | Classificação | Notas |
|---|---|---|---|---|---|
| 1 | O período deve conter mês entre 1 e 12. | SE o período informado contiver mês fora de 01 a 12, ENTÃO o cálculo DEVE retornar erro de período inválido. | `legacy-sifap/natural-programs/CALCBENF.NSN:176-181` | Confirmada | Código de retorno `2020`. |
| 2 | O beneficiário precisa estar ativo. | SE a situação do beneficiário for diferente de `A`, ENTÃO o cálculo DEVE rejeitar a operação. | `legacy-sifap/natural-programs/CALCBENF.NSN:201-207` | Confirmada | O DDM `BENEFIC` define os estados cadastrais. |
| 3 | O valor bruto combina base e fatores de cálculo. | QUANDO o beneficiário e o programa forem válidos, o sistema DEVE calcular o valor bruto com os fatores regional, familiar, renda, idade e ajuste do programa. | `legacy-sifap/natural-programs/CALCBENF.NSN:260-276` | Confirmada | O resultado é truncado para duas casas. |
| 4 | Dezembro gera pagamento adicional. | QUANDO o período for dezembro, o sistema DEVE calcular o adicional de dezembro e marcar o tipo como `D`. | `legacy-sifap/natural-programs/CALCBENF.NSN:280-292` | Confirmada | A fórmula observada não usa meses ativos. |
| 5 | Programa tipo `A` recebe abono de 15% em dezembro. | QUANDO o período for dezembro e o programa for do tipo `A`, o sistema DEVE adicionar abono de 15% ao bruto. | `legacy-sifap/natural-programs/CALCBENF.NSN:294-302` | Confirmada | O abono é truncado. |
| 6 | O valor líquido não pode ser negativo. | SE os descontos excederem o bruto, ENTÃO o sistema DEVE retornar líquido igual a zero. | `legacy-sifap/natural-programs/CALCBENF.NSN:307-316` | Confirmada | — |
| 7 | Existe uma dedução simplificada no cálculo principal. | QUANDO o fluxo atual executar `CALCBENF`, o sistema DEVE aplicar a regra efetivamente conectada ao fluxo. | `legacy-sifap/natural-programs/CALCBENF.NSN:347-357` | Mistério | A coexistência com `CALCDSCT` precisa de decisão humana. |

## Regras de `CALCDSCT.NSP`

| # | Enunciado da regra | Candidato EARS | Origem | Classificação | Notas |
|---|---|---|---|---|---|
| 1 | A contribuição social usa faixas de 3%, 5%, 7% e 9%. | QUANDO o desconto social for calculado, o sistema DEVE selecionar a primeira faixa aplicável e aplicar sua taxa. | `legacy-sifap/natural-programs/CALCDSCT.NSP:57-64;210-218` | Confirmada | — |
| 2 | Descontos fora da vigência são ignorados. | SE a data final já tiver passado ou a data inicial ainda não tiver chegado, ENTÃO o desconto DEVE ser ignorado. | `legacy-sifap/natural-programs/CALCDSCT.NSP:126-137` | Confirmada | — |
| 3 | Desconto judicial pode ser fixo ou percentual. | QUANDO o tipo for `J`, o sistema DEVE usar o valor fixo quando informado; caso contrário, DEVE calcular pelo percentual. | `legacy-sifap/natural-programs/CALCDSCT.NSP:141-153` | Confirmada | — |
| 4 | Descontos não judiciais têm teto de 30%. | SE o acumulado não judicial exceder 30% do bruto, ENTÃO o sistema DEVE limitá-lo ao teto. | `legacy-sifap/natural-programs/CALCDSCT.NSP:182-189` | Confirmada | O tipo `J` é exceção explícita. |

## Regras de `CALCCORR.NSP`

| # | Enunciado da regra | Candidato EARS | Origem | Classificação | Notas |
|---|---|---|---|---|---|
| 1 | O período inicial não pode ser posterior ao final. | SE o início for maior que o fim, ENTÃO a correção DEVE ser rejeitada. | `legacy-sifap/natural-programs/CALCCORR.NSP:105-109` | Confirmada | — |
| 2 | CPF inválido impede a correção. | SE a validação do CPF falhar, ENTÃO a correção DEVE ser rejeitada. | `legacy-sifap/natural-programs/CALCCORR.NSP:112-125` | Confirmada | Usa `SUBVALCP`. |
| 3 | Pagamentos já corrigidos não são processados novamente. | SE o indicador de correção for `S`, ENTÃO o sistema DEVE ignorar o pagamento. | `legacy-sifap/natural-programs/CALCCORR.NSP:139-141` | Confirmada | — |
| 4 | Correção positiva atualiza pagamento e auditoria. | SE a diferença corrigida for maior que zero, ENTÃO o sistema DEVE atualizar o pagamento e registrar auditoria. | `legacy-sifap/natural-programs/CALCCORR.NSP:165-184` | Confirmada | — |

## Regras de `BATCHPGT.NSP`

| # | Enunciado da regra | Candidato EARS | Origem | Classificação | Notas |
|---|---|---|---|---|---|
| 1 | Beneficiários inativos são ignorados. | ENQUANTO o beneficiário não estiver com situação `A`, o lote DEVE ignorá-lo. | `legacy-sifap/natural-programs/BATCHPGT.NSP:258-271` | Confirmada | — |
| 2 | CPF inválido gera rejeição. | SE a validação do CPF falhar, ENTÃO o lote DEVE registrar erro em `CMWKF02` e não gerar pagamento. | `legacy-sifap/natural-programs/BATCHPGT.NSP:276-295` | Confirmada | — |
| 3 | Pagamento existente para CPF e período impede duplicidade. | SE já existir pagamento para CPF + período, ENTÃO o lote DEVE ignorar o beneficiário. | `legacy-sifap/natural-programs/BATCHPGT.NSP:297-305` | Confirmada | Usa o superdescritor `S1`. |
| 4 | Pagamento gerado recebe status `G`. | QUANDO o cálculo terminar com sucesso, o lote DEVE gravar o pagamento com status `G` e os valores calculados. | `legacy-sifap/natural-programs/BATCHPGT.NSP:433-457` | Confirmada | — |
| 5 | A elegibilidade é validada antes do cálculo. | QUANDO o lote processar um beneficiário aprovado na validação de CPF, o sistema DEVE chamar `VALELEG` e ignorar o beneficiário quando o retorno for diferente de zero. | `legacy-sifap/natural-programs/BATCHPGT.NSP:369-379` | Confirmada | `CALLNAT` incluído pelo chamado 6621/2011. O beneficiário reprovado entra em `#QTY-IGNORED`, não em `#QTY-ERRS`. |

## Regras de `VALELEG.NSN`

Leitura de apoio. `VALELEG` é atribuído à Dupla 4; as regras abaixo foram
extraídas porque a rotina integra o caminho de produção da geração mensal.

| # | Enunciado da regra | Candidato EARS | Origem | Classificação | Notas |
|---|---|---|---|---|---|
| 1 | Beneficiário inexistente impede a validação. | SE o CPF não existir no cadastro, ENTÃO a validação DEVE retornar `2001`. | `legacy-sifap/natural-programs/VALELEG.NSN:84-89` | Confirmada | — |
| 2 | Programa inexistente impede a validação. | SE o programa não existir, ENTÃO a validação DEVE retornar `2003`. | `legacy-sifap/natural-programs/VALELEG.NSN:100-105` | Confirmada | — |
| 3 | Programa inativo impede a elegibilidade. | SE a situação do programa for diferente de `A`, ENTÃO a validação DEVE retornar `2004`. | `legacy-sifap/natural-programs/VALELEG.NSN:114-118` | Confirmada | Verificado antes de qualquer regra do beneficiário. |
| 4 | Região `99` dispensa todas as validações restantes. | QUANDO a região do beneficiário for `99`, o sistema DEVE declará-lo elegível e encerrar a validação. | `legacy-sifap/natural-programs/VALELEG.NSN:120-128` | Mistério | Sem regra de negócio conhecida. Registrado em `SIFAP-M-12`. |
| 5 | Situação cadastral diferente de `A` torna inelegível. | SE a situação do beneficiário for `S`, `C`, `D` ou `I`, ENTÃO o sistema DEVE marcá-lo inelegível com o motivo correspondente. | `legacy-sifap/natural-programs/VALELEG.NSN:133-151` | Confirmada | Situações fora dessas cinco não geram motivo e permanecem elegíveis. |
| 6 | A faixa etária do programa é opcional. | ENQUANTO a idade mínima ou máxima do programa for maior que zero, o sistema DEVE recusar o beneficiário fora da faixa. | `legacy-sifap/natural-programs/VALELEG.NSN:156-169` | Confirmada | O valor zero desativa o limite. |
| 7 | O teto de renda familiar do programa é opcional. | ENQUANTO o teto de renda do programa for maior que zero, o sistema DEVE recusar renda familiar superior ao teto. | `legacy-sifap/natural-programs/VALELEG.NSN:174-180` | Confirmada | Compara renda familiar, apesar de o campo do programa se chamar `MAX-PERCAP-INCOME`. |
| 8 | Programa tipo `A` exige documentação e restringe renda sem dependentes. | QUANDO o programa for do tipo `A`, o sistema DEVE recusar documentação incompleta e recusar renda acima de 600,00 quando não houver dependentes. | `legacy-sifap/natural-programs/VALELEG.NSN:186-200` | Confirmada | Renda acima de 600,00 é aceita se houver ao menos um dependente. |
| 9 | Programa tipo `P` exige idade mínima de 60 anos. | QUANDO o programa for do tipo `P`, o sistema DEVE recusar idade inferior a 60. | `legacy-sifap/natural-programs/VALELEG.NSN:201-207` | Confirmada | Limite fixo no código, independente de `AGE-MIN`. |
| 10 | Programa tipo `T` exige idade entre 16 e 65 anos. | QUANDO o programa for do tipo `T`, o sistema DEVE recusar idade fora de 16 a 65. | `legacy-sifap/natural-programs/VALELEG.NSN:208-214` | Confirmada | Limites fixos no código. |
| 11 | Tipo de programa desconhecido torna inelegível. | SE o tipo do programa não for `A`, `P` nem `T`, ENTÃO o sistema DEVE marcar o beneficiário como inelegível. | `legacy-sifap/natural-programs/VALELEG.NSN:215-219` | Confirmada | — |
| 12 | O código de elegibilidade exige NIS e dependentes por posição. | QUANDO o código de elegibilidade tiver `R` na primeira posição, o sistema DEVE exigir NIS cadastrado; quando tiver `D` na segunda, DEVE exigir ao menos um dependente. | `legacy-sifap/natural-programs/VALELEG.NSN:248-262` | Confirmada | As demais posições do código não são interpretadas. |
| 13 | Apenas o primeiro motivo de recusa é devolvido. | QUANDO o beneficiário for inelegível, o sistema DEVE retornar `2010` com o primeiro motivo acumulado. | `legacy-sifap/natural-programs/VALELEG.NSN:231-237` | Confirmada | Os demais motivos são coletados e descartados. |

> [!NOTE]
> Duplique a seção acima para cada programa `.NSP` ou `.NSN` lido pela sua dupla.

---

## Resumo geral

| Métrica | Valor |
|---|---:|
| Programas Natural lidos | 5 |
| DDMs cruzados | 3 (`BENEFIC`, `PAYMENT`, `SOCPROG`) |
| Regras confirmadas | 31 |
| Regras inferidas | 0 |
| Mistérios | 2 (dedução concorrente; desvio da região `99`) |

> [!WARNING]
> Este catálogo cobre somente o recorte investigado nesta sessão. Ele não substitui a leitura atribuída das demais duplas.

---

## Definição de pronto

- [ ] Todo bloco condicional dos programas atribuídos foi examinado.
- [ ] Toda regra cita `arquivo:linha`.
- [ ] Toda questão em aberto está registrada em `mysteries-found.md` sem conclusão.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Inventário](inventory.md)<br/><sub>Passo 1 — varredura de arquivos.</sub> | [Mapa de Dependências](dependency-map.md)<br/><sub>Passo 3 — grafo de chamadas e acessos.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
