# Especificação — Consulta de beneficiário

Modernização da tela 3270 `CONSBENF`, que consulta o cadastro do beneficiário
e o histórico recente de pagamentos.

| Campo | Valor |
|---|---|
| **Feature** | `004-consulta-beneficiario` |
| **Programa legado** | `CONSBENF.NSP` |
| **Requisitos** | `REQ-034` a `REQ-042` |
| **Depende de** | Features `001` e `003` (cadastro e pagamentos já existem) |

---

## Contexto

`CONSBENF` é uma transação **online**, não agendada em `SIFAPJ01` nem
`SIFAPJ02` (`CONSBENF.NSP:15-16`). É a única tela do corpus lido que entrega
dados ao público interno: busca por CPF ou NIS, exibe o cadastro e lista os
pagamentos mais recentes.

É a âncora legada natural para a primeira interface do sistema moderno, porque
substitui uma tela que existe e é operada hoje, em vez de inventar uma.

---

## Requisitos

### REQ-034 (orientado a evento) — Consultar beneficiário por CPF

QUANDO uma consulta por CPF for solicitada, o sistema DEVE retornar o cadastro
do beneficiário correspondente.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CONSBENF.NSP#L147-L155

**Critérios de aceitação**

- AC-034.1: Dado um CPF cadastrado, quando a consulta for solicitada, então o cadastro deve ser retornado.
- AC-034.2: Dado um CPF válido e não cadastrado, quando a consulta for solicitada, então o resultado deve indicar beneficiário não encontrado.

### REQ-035 (orientado a evento) — Consultar beneficiário por NIS

QUANDO uma consulta por NIS for solicitada, o sistema DEVE retornar o cadastro
do beneficiário correspondente.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CONSBENF.NSP#L156-L163

**Critérios de aceitação**

- AC-035.1: Dado um NIS cadastrado, quando a consulta for solicitada, então o cadastro deve ser retornado.
- AC-035.2: Dado um NIS não cadastrado, quando a consulta for solicitada, então o resultado deve indicar beneficiário não encontrado.

> O legado não valida o NIS antes de buscar: `SUBVALCP` só é acionado no ramo
> de CPF (`CONSBENF.NSP:132-144`). O comportamento é preservado.

### REQ-036 (orientado a evento) — Rejeitar CPF inválido antes da busca

QUANDO uma consulta por CPF com dígito verificador inválido for solicitada, o
sistema DEVE rejeitar a consulta sem acessar o cadastro.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CONSBENF.NSP#L132-L144

**Critérios de aceitação**

- AC-036.1: Dado um CPF com dígito verificador inválido, quando a consulta for solicitada, então ela deve ser rejeitada.
- AC-036.2: Dado um CPF inválido, quando a consulta for rejeitada, então o cadastro não deve ser acessado.

### REQ-037 (ubíquo) — Mascarar o CPF na exibição

O sistema DEVE exibir o CPF do beneficiário mascarado, revelando apenas os
cinco últimos dígitos, no formato `***.***.XXX-XX`.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CONSBENF.NSP#L292-L311

**Critérios de aceitação**

- AC-037.1: Dado o CPF `52998224725`, quando o cadastro for exibido, então o CPF deve aparecer como `***.***.247-25`.
- AC-037.2: Dado qualquer CPF, quando o cadastro for exibido, então os seis primeiros dígitos não devem aparecer.

> **Divergência deliberada.** O legado tem uma inconsistência conhecida: quando
> o CPF armazenado tem menos de 11 dígitos, a máscara revela os **três
> primeiros** dígitos em vez dos últimos (`CONSBENF.NSP:298-301`). O comentário
> do código pede que não seja corrigida sem aprovação de auditoria. O sistema
> moderno não replica esse ramo: a máscara é sempre consistente. Justificativa
> no plano técnico; achado registrado em `mysteries-found.md`.

### REQ-038 (ubíquo) — Descrever a situação cadastral

O sistema DEVE apresentar a situação cadastral do beneficiário com o código
armazenado e sua descrição.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CONSBENF.NSP#L228-L245

**Critérios de aceitação**

- AC-038.1: Dada a situação `A`, quando o cadastro for exibido, então a descrição deve ser `Ativo`.
- AC-038.2: Dada a situação `S`, quando o cadastro for exibido, então a descrição deve ser `Suspenso`.
- AC-038.3: Dada uma situação fora de `A`, `S`, `C`, `I` e `D`, quando o cadastro for exibido, então a descrição deve ser `Desconhecido`.

### REQ-039 (ubíquo) — Limitar o histórico a doze pagamentos

O sistema DEVE apresentar no máximo doze pagamentos no histórico do
beneficiário.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CONSBENF.NSP#L270-L284

**Critérios de aceitação**

- AC-039.1: Dado um beneficiário com quinze pagamentos, quando o histórico for exibido, então exatamente doze devem aparecer.
- AC-039.2: Dado um beneficiário com cinco pagamentos, quando o histórico for exibido, então os cinco devem aparecer.

### REQ-040 (ubíquo) — Ordenar o histórico do período mais recente para o mais antigo

O sistema DEVE ordenar o histórico de pagamentos do período mais recente para
o mais antigo.

source_legacy: "[GREENFIELD] O legado rotula o bloco como LAST 12, mas o READ percorre pelo descritor de CPF sem ordenar por período; achado BONUS registrado em mysteries-found.md."

**Critérios de aceitação**

- AC-040.1: Dados pagamentos dos períodos `202601`, `202603` e `202602`, quando o histórico for exibido, então a ordem deve ser `202603`, `202602`, `202601`.
- AC-040.2: Dado um beneficiário com quinze pagamentos, quando o histórico for exibido, então os doze períodos mais recentes devem aparecer.

### REQ-041 (orientado a evento) — Informar ausência de pagamentos

QUANDO um beneficiário sem pagamentos for consultado, o sistema DEVE indicar
explicitamente que não há pagamentos, em vez de exibir uma lista vazia.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CONSBENF.NSP#L286-L288

**Critérios de aceitação**

- AC-041.1: Dado um beneficiário sem pagamentos, quando o histórico for exibido, então deve haver indicação explícita de ausência.

### REQ-042 (orientado a evento) — Registrar trilha de acesso a dados pessoais

QUANDO uma consulta de beneficiário for concluída com sucesso, o sistema DEVE
registrar o acesso na trilha de auditoria.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CONSBENF.NSP#L168-L179

**Critérios de aceitação**

- AC-042.1: Dada uma consulta bem-sucedida, quando ela for concluída, então um registro de auditoria deve ser criado com a ação `CO` e a entidade `BENF`.
- AC-042.2: Dada uma consulta que não encontrou o beneficiário, quando ela for concluída, então nenhum registro de auditoria deve ser criado.

> O legado grava a trilha depois do `DECIDE`, e um beneficiário não encontrado
> provoca `REINPUT`, que reinicia o laço antes de alcançar o bloco de
> auditoria. A exigência vem da IN-TCU 63/2010, citada no próprio código.

---

## Fora de escopo

| Item | Motivo |
|---|---|
| Edição de cadastro | `CADBENEF` é outro programa, fora desta feature |
| Consulta de dependentes | `CADDEPEN` não foi lido |
| Endereço do beneficiário | O DDM tem os campos, mas a base moderna não os armazena; incluir exigiria migração de cadastro sem regra de negócio associada |
| Paginação do histórico | O legado corta em doze sem oferecer navegação |
| Autenticação de quem consulta | Não há evidência de controle de acesso no programa lido; a trilha registra o usuário da sessão Natural, que não existe no sistema moderno |

---

## Rastreabilidade

| REQ-ID | Origem |
|---|---|
| `REQ-034` a `REQ-039` | `CONSBENF.NSP` |
| `REQ-040` | Correção deliberada de comportamento observado |
| `REQ-041`, `REQ-042` | `CONSBENF.NSP` |
