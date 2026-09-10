# Registro de Questões em Aberto — Estágio 1

> **Trilha:** [Kit do Time](../README.md) › [Estágio 1](README.md) › **Questões em Aberto**

**Registro rastreável das incertezas do Estágio 1.** Cada entrada documenta uma pergunta sem resposta, com evidência, hipótese marcada como não confirmada e responsável pela validação.

| Campo | Valor |
|---|---|
| **Público-alvo** | Todas as duplas |
| **Pré-requisitos** | Ler os programas atribuídos |
| **Estágio** | Estágio 1 — Arqueologia |
| **Resultado esperado** | Perguntas sem conclusão, com evidência e responsável identificado |

> [!IMPORTANT]
> Uma pergunta só vira regra de negócio, requisito ou conclusão depois de validação humana explícita e com a evidência preservada como `path:line`. Este registro não é uma resposta e não substitui essa validação.

---

## Registro

Use uma linha por mistério. Preencha com o **ID canônico** da sua dupla (`SIFAP-M-01` … `SIFAP-M-20` — veja o [checklist](mysteries-checklist.md)) ou `BONUS` para achados fora da lista.

| ID | Questão em aberto | Evidência (`path:line`) | Impacto | Hipótese (não confirmada) | Pessoa/área responsável | Status |
|---|---|---|---|---|---|---|
| `SIFAP-M-09` | `CALCDSCT` substitui ou complementa a dedução simplificada do fluxo mensal? **Questão técnica resolvida por evidência:** o job mensal `SIFAPJ01` executa apenas `BATCHPGT`, que aplica a dedução simplificada inline e gera a remessa bancária com esse líquido; `CALCDSCT` é programa interativo, disparado por operador, e não integra o caminho de produção. A documentação de 2012 afirma o contrário e está incorreta. **Permanece aberta a decisão de negócio:** a dedução simplificada é a regra oficial ou um defeito tolerado desde 1999? | `legacy-sifap/natural-programs/CALCBENF.NSN:357-366`; `legacy-sifap/natural-programs/CALCDSCT.NSP:62-69`; `legacy-sifap/natural-programs/CALCDSCT.NSP:71-75`; `legacy-sifap/natural-programs/BATCHPGT.NSP:455-500`; `legacy-sifap/natural-programs/SIFAPJ01.jcl:70-77`; `legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md:220` | Adotar a rotina detalhada criaria desconto para beneficiários com bruto até 500,00, faixa de menor renda que hoje não tem dedução. Preservar a simplificada perpetua desconto possivelmente subaplicado desde 1999. | Não confirmada: proposta registrada em `docs/adr/0004-simplified-deduction-monthly-flow.md` recomenda preservar o comportamento observado e manter `CALCDSCT` como recálculo sob demanda. | Coordenação de benefícios + operação do batch | proposta registrada em ADR-0004 — aguardando ratificação humana |
| `SIFAP-M-10` | Por que o batch legado manteve uma fórmula inline ativa após chamar `CALCBENF`? | `legacy-sifap/natural-programs/BATCHPGT.NSP:330-425`; `legacy-sifap/natural-programs/CALCBENF.NSN:260-316` | A duplicação pode gerar divergências de cálculo no legado; reproduzi-la em Java criaria duas fontes de verdade. | Não confirmada: a implementação moderna centraliza a fórmula em um serviço único; a razão histórica da duplicação continua não confirmada. | Arquitetura + mantenedor do batch | fechada para a feature atual; aberta para arqueologia histórica |
| `SIFAP-M-11` | A proporcionalidade do décimo-terceiro deve ser criada como regra nova ou descartada formalmente? | `legacy-sifap/natural-programs/CALCBENF.NSN:280-292`; `legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md:255-270` | Benefícios iniciados no meio do ano podem ser pagos de forma diferente se a regra for criada agora. | Não confirmada: para a feature atual, preserva-se o código observado sem proporcionalidade; regra nova exige aprovação de negócio. | Coordenação de benefícios | aguardando validação humana |
| `SIFAP-M-12` | A região `99` possui significado operacional além do fator neutro observado no cálculo? **Sim — evidência encontrada em `VALELEG` e reproduzida no sistema moderno.** No cálculo, `99` cai na faixa fora de 1 a 25 e recebe fator neutro `1.0000`. Na validação de elegibilidade, `99` provoca saída antecipada que **ignora todas as verificações seguintes**: faixa etária, teto de renda, regras por tipo de programa, documentação, NIS e dependentes. O desvio ocorre depois da checagem de programa inativo e antes de todo o restante. **Permanece aberta a decisão de negócio:** o desvio é regra legítima para registros diplomáticos/internacionais ou bypass administrativo indevido? A documentação de 2012 registra que o autor da regra não soube explicar sua origem. | `legacy-sifap/natural-programs/CALCBENF.NSN:218-231`; `legacy-sifap/natural-programs/VALELEG.NSN:120-128`; `legacy-sifap/natural-programs/BATCHPGT.NSP:369-379`; `legacy-sifap/natural-programs/LDASIFAP.NSL:38-48`; `legacy-sifap/adabas-ddms/BENEFIC.ddm:76-86`; `legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md:196-202` | No fluxo mensal, o beneficiário inativo já é filtrado por `BATCHPGT` antes da chamada, então o desvio **não** ressuscita cadastro suspenso nesse caminho. Ele dispensa idade, renda, tipo de programa, documentação, NIS e dependentes — um beneficiário de região `99` recebe pagamento sem nenhuma dessas validações. **Reprodução executável:** o beneficiário `15350946056`, semeado em `db/dev/V6`, tem 26 anos em programa que exige 60, renda de `9.000,00` contra teto de `2.000,00`, nenhum NIS e nenhum dependente, e o código de elegibilidade `RD` exige ambos. Viola quatro regras e ainda assim recebe pagamento de `40,00`. | Não confirmada: o comentário do código diz `INTERNATIONAL/DIPLOMATIC`, mas nenhuma regra de negócio localizada autoriza dispensar as validações. A documentação de 2012 levanta a hipótese de mecanismo de teste ou bypass administrativo, sem confirmação. | Coordenação de benefícios + DBA + auditoria | evidência técnica registrada e reproduzível — decisão de negócio aguardando validação humana |

### Achados adicionais (bônus)

Achados legítimos fora dos 20 mistérios canônicos. Contam no debrief, **não** mudam o denominador e **não** substituem um mistério canônico que ficou faltando.

| ID | Questão em aberto | Evidência (`path:line`) | Impacto | Hipótese (não confirmada) | Pessoa/área responsável | Status |
|---|---|---|---|---|---|---|
| `BONUS` | A tabela de índices IPCA cobre o período necessário para correções retroativas atuais? | `legacy-sifap/natural-programs/CALCCORR.NSP:86-104`; `legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md:219-230` | Correções podem ser calculadas com índice ausente. | Não confirmada: o código observado contém anos limitados e pode depender de manutenção manual. | Coordenação financeira + mantenedor de índices | aberta |
| `BONUS` | O teto de 30% deve poder reduzir descontos judiciais já acumulados, como o código observado permite? | `legacy-sifap/natural-programs/CALCDSCT.NSP:128-137`; `legacy-sifap/natural-programs/CALCDSCT.NSP:169-174` | O teto é aplicado dentro do laço sempre que o item corrente não é `J`. Como o total é acumulado, um item posterior não judicial pode truncar valor originado de um desconto judicial, que a própria regra declara isento de teto. A ordem de cadastro dos itens altera o líquido. | Não confirmada: pode ser efeito colateral não intencional da aplicação do teto por item em vez de ao final; a intenção declarada no comentário é isentar `J`. | Coordenação de benefícios + jurídico | aberta |
| `BONUS` | Um pagamento recalculado por `CALCDSCT` diverge da remessa bancária já transmitida. Existe procedimento de conciliação? | `legacy-sifap/natural-programs/BATCHPGT.NSP:489-500`; `legacy-sifap/natural-programs/CALCDSCT.NSP:179-188` | `BATCHPGT` grava a remessa `CMWKF01` com o líquido simplificado. Um recálculo posterior atualiza `AMT-DISC-TOTAL` e `AMT-NET` do pagamento, mas nada regenera a remessa. O registro passa a divergir do valor transmitido ao banco. | Não confirmada: nenhum mecanismo de regeneração ou conciliação foi localizado no código lido. Pode existir procedimento operacional fora do código. | Coordenação financeira + operação do batch | aberta |
| `BONUS` | `VALELEG` recebe idade, renda, dependentes, região e situação por PDA, mas sobrescreve todos esses valores com a leitura do arquivo 150. Os parâmetros enviados por `BATCHPGT` são descartados. Isso é intencional? | `legacy-sifap/natural-programs/VALELEG.NSN:75-96`; `legacy-sifap/natural-programs/BATCHPGT.NSP:356-379`; `legacy-sifap/natural-programs/BATCHPGT.NSP:336-348` | Consequência concreta na idade: `BATCHPGT` aplica a janela de século Y2K antes de calcular a idade; `VALELEG` calcula a idade direto de `DT-BIRTH` sem essa janela. Para cadastros históricos ainda gravados como `YYMMDD`, os dois programas obtêm idades diferentes no mesmo processamento, e a elegibilidade por faixa etária é decidida pela idade não corrigida. | Não confirmada: pode ser resíduo da conversão para subprograma no chamado 6621/2011, quando a rotina deixou de ser interativa e passou a reler o cadastro. A duplicação da leitura sugere que o contrato do PDA nunca foi revisto. | Arquitetura + mantenedor do batch | aberta |
| `BONUS` | A documentação de 2012 descreve regras de elegibilidade que não existem no código de `VALELEG`. Elas foram removidas, nunca implementadas ou vivem em outro programa? | `legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md:186-196`; `legacy-sifap/natural-programs/VALELEG.NSN:120-262` | O documento afirma que `VALELEG` valida dados bancários, limite de 2 programas simultâneos (`BN-QT-PROG`), atualização cadastral em até 24 meses (`BN-DT-ULT-ATUAL`) e ocorrência de auditoria bloqueante. Nenhuma dessas verificações existe no código lido. O documento também estima 1.200 linhas para um programa com cerca de 265. Modernizar a partir do documento criaria regras inexistentes e recusaria beneficiários hoje aprovados. | Não confirmada: o mesmo documento já se mostrou incorreto sobre a cadeia de descontos, conforme `SIFAP-M-09`. Pode descrever uma versão planejada e não entregue, ou outro programa de validação. | Coordenação de benefícios + arquitetura | aberta |
| `BONUS` | A tabela de fatores regionais tem 27 entradas e a consulta aceita 1 a 25, mas o DDM restringe o domínio do campo a `01-05` ou `99`. Quais regiões existem de fato? | `legacy-sifap/natural-programs/BATCHPGT.NSP:192-218`; `legacy-sifap/natural-programs/BATCHPGT.NSP:390-394`; `legacy-sifap/adabas-ddms/BENEFIC.ddm:69`; `legacy-sifap/adabas-ddms/SOCPROG.ddm:78-84` | Achado de dois lados. Se o DDM estiver correto, os fatores das posições 6 a 25 nunca são usados e as posições 26 e 27 são inalcançáveis pela própria consulta. O `SOCPROG` ainda define parâmetros regionais por programa, incluindo fator e complemento, que o cálculo ignora em favor da tabela fixa no código. Uma futura carga com região `06` passaria a aplicar fator `1,4000` sem que nenhuma regra de negócio tenha autorizado isso. | Não confirmada: a tabela pode ser resíduo de um modelo regional mais granular abandonado, ou o DDM pode estar desatualizado. Nenhuma fonte lida explica as 27 posições. | Coordenação de benefícios + DBA | aberta |

---

## Regras de integridade

- Registre apenas questões em aberto; não escreva uma resposta no catálogo.
- Mantenha a evidência no formato `path:line` para preservar a rastreabilidade.
- Marque toda hipótese explicitamente como **não confirmada**.
- Só a pessoa responsável pode dar a validação humana e mudar o status.
- Sem evidência humana, a questão continua em aberto.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Checklist de Questões em Aberto](mysteries-checklist.md)<br/><sub>Verificação de rastreabilidade.</sub> | [Relatório de Descoberta](discovery-report.md)<br/><sub>Consolidação final do estágio.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
