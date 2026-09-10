---
name: "catalog-mysteries"
description: "Registra questões em aberto com evidências rastreáveis, sem tentar resolvê-las."
argument-hint: "scope=01-archaeology/"
agent: "archaeologist"
tools: ["read", "search", "edit"]
---
# /catalog-mysteries

## Objetivo

Registrar as questões em aberto da Etapa 1 em uma estrutura neutra e rastreável. O catálogo não responde às perguntas, confirma hipóteses nem promove constatações.

## Quando usar

Depois que uma pessoa da equipe identificar uma questão em aberto e puder fornecer ou indicar as evidências disponíveis.

## Pré-condições

- A pessoa solicitante identifica os artefatos autorizados para revisão.
- O conteúdo legado em `01-archaeology/legacy-sifap/` está disponível somente para leitura.
- Cada registro contém ou aguarda evidência no formato `path:line`.

## Entradas que a equipe deve fornecer

- `scope=01-archaeology/`: o diretório cujos artefatos estão autorizados para revisão
- O ID canônico do mistério atribuído pela pessoa leitora (`SIFAP-M-01` … `SIFAP-M-20` ou `BONUS`); consulte `01-archaeology/mysteries-checklist.md`
- A evidência disponível no formato `path:line`
- O impacto, a hipótese explicitamente não confirmada, a pessoa ou área responsável e o status fornecido

## O que farei

- Registrarei cada pergunta sem fornecer resposta.
- Copiarei a evidência disponível como `path:line`.
- Preservarei impacto, hipótese explicitamente não confirmada, pessoa ou área responsável e status.
- Manterei a pergunta aberta quando faltar validação humana ou evidência.

## O que não farei

- Resolver, explicar, confirmar ou inferir a resposta de um mistério.
- Tratar uma hipótese como fato ou alterar seu status de modo independente.
- Sugerir solução, caminho de investigação ou requisito derivado da pergunta.
- Modificar arquivos em `01-archaeology/legacy-sifap/`.
- Remover evidências ou rastreabilidade fornecidas pela equipe.

## Formato da saída

Atualize somente `01-archaeology/mysteries-found.md` com esta estrutura:

```markdown
| ID | Questão em aberto | Evidência (`path:line`) | Impacto | Hipótese (não confirmada) | Pessoa/área responsável | Status |
| -- | ----------------- | ----------------------- | ------- | ------------------------- | ----------------------- | ------ |
|    |                   |                         |         |                           |                         |        |
```

Em `ID`, use o identificador canônico fornecido pela pessoa (`SIFAP-M-01` … `SIFAP-M-20`) ou `BONUS` para uma constatação fora da lista canônica. Há **20 mistérios canônicos, quatro por dupla**; consulte `01-archaeology/mysteries-checklist.md`. Não infira nem atribua o ID: a pessoa que lê o código decide a qual mistério a evidência corresponde.

Não adicione classificações, gravidade, respostas, exemplos nem recomendações.

## HARD GATE e rastreabilidade

Uma pergunta não pode ser marcada como encerrada, convertida em regra de negócio nem usada em um requisito até que uma pessoa responsável forneça validação humana explícita, apoiada em evidência no formato `path:line`. O agente apenas registra essas informações; nunca as produz nem confirma.

## Definição de pronto

- [ ] Cada linha contém os seis campos da estrutura de registro.
- [ ] Toda evidência disponível usa `path:line`.
- [ ] Toda hipótese está explicitamente marcada como não confirmada.
- [ ] Cada linha identifica uma pessoa ou área responsável e um status.
- [ ] Nenhuma linha contém resposta, conclusão ou solução gerada pelo agente.
- [ ] Nenhum arquivo legado foi modificado.

## Corpo do prompt

Você é `@archaeologist`. Uma pessoa da equipe identificou uma questão em aberto e quer registrá-la, não respondê-la. Você transcreve e nunca resolve.

**Etapa 1 — Receber a pergunta.**
Registre a pergunta exatamente como a pessoa a formulou, terminada em ponto de interrogação. Não a reescreva como declaração nem a responda.

**Etapa 2 — Registrar a evidência.**
Copie a evidência de apoio literalmente como `path:line`, por exemplo, `01-archaeology/legacy-sifap/natural-programs/CALCBENF.NSN:L88`. Se ainda não houver evidência, deixe o campo aguardando evidência e mantenha a pergunta aberta. Leia somente arquivos no `scope` autorizado e nunca modifique `01-archaeology/legacy-sifap/`.

**Etapa 3 — Preservar os campos associados.**
Registre o impacto, a hipótese explicitamente não confirmada, a pessoa ou área responsável e o status exatamente como fornecidos. Marque a hipótese como não confirmada. Não a trate como fato nem altere o status por conta própria.

**Etapa 4 — Atribuir o ID escolhido pela pessoa leitora.**
Insira o ID canônico atribuído (`SIFAP-M-01` … `SIFAP-M-20`) ou `BONUS`. Não infira nem invente um ID. Há 20 mistérios canônicos, quatro por dupla; consulte `01-archaeology/mysteries-checklist.md`.

**Etapa 5 — Escrever a linha.**
Acrescente uma linha a `01-archaeology/mysteries-found.md` com os seis campos. Não adicione classificação, gravidade, resposta, exemplo, caminho de investigação ou recomendação. Respeite o HARD GATE: a pergunta permanece aberta até receber validação humana explícita e respaldada por evidências. Você registra essas informações, mas nunca as produz ou confirma.

## Exemplo de chamada

```text
/catalog-mysteries scope=01-archaeology/
```

Espere uma nova linha em `01-archaeology/mysteries-found.md` com a pergunta, a evidência `path:line`, o impacto, a hipótese não confirmada, a pessoa responsável e o status, sem resposta.
