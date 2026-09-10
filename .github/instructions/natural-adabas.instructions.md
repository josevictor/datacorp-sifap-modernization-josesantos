---
description: "Use ao ler código legado Natural/Adabas, padrões da linguagem, estrutura FDT, convenções de nomenclatura e fluxos batch."
applyTo: "01-archaeology/legacy-sifap/**,**/*.NSP,**/*.nsp,**/*.NSN,**/*.nsn,**/*.NSS,**/*.nss,**/*.NSA,**/*.nsa,**/*.NSL,**/*.nsl,**/*.NSC,**/*.nsc,**/*.NSM,**/*.nsm,**/*.NSD,**/*.nsd,**/*.NAT,**/*.nat,**/*.CPY,**/*.cpy,**/*.DDM,**/*.ddm,**/*.jcl,**/*.JCL"
---

# Código legado Natural/Adabas — Guia de leitura

Este arquivo é ativado quando você abre programas Natural, DDMs Adabas, JCL, copycodes ou qualquer arquivo no diretório `01-archaeology/legacy-sifap/`. Ele ensina a ler código legado do SIFAP (Sistema de Fiscalização e Administração de Pagamentos): estrutura de programas Natural, dependências CALLNAT e INCLUDE, FDTs Adabas, nomenclatura legada, padrões batch, decimais compactados e estratégia de primeira leitura. Ele **não** decide limites de módulos modernos nem mapeamentos JPA, que pertencem a [`modular-monolith.instructions.md`](modular-monolith.instructions.md), e não escreve requisitos EARS nem registros de rastreabilidade, que pertencem a [`requirements.instructions.md`](requirements.instructions.md).

## Estrutura de programas Natural

Um programa Natural segue este esqueleto:

```
DEFINE DATA
  LOCAL
    01 #MY-VARIABLE  (A20)    /* A = alfanumérico, 20 caracteres */
    01 #COUNTER      (N5)     /* N = numérico, 5 dígitos */
    01 #AMOUNT       (P9.2)   /* P = decimal compactado, 9 inteiros + 2 decimais */
    01 #RATES        (N3.4/1:27)  /* array: 27 ocorrências de N3.4 */
  END-DEFINE

  /* Lógica principal aqui */

END
```

> **Neste laboratório, o separador decimal em uma especificação de formato é o ponto.**
> Natural Community Edition 9.3.3 compila `(P9.2)` e `(N3.4)`. Ele rejeita `(P9,2)` com `NAT0165`.
> Instalações Natural podem variar conforme a configuração do caractere decimal; esta imersão segue a imagem Community Edition.
> Esta regra se aplica somente à *declaração*; **literais também usam ponto**: `MOVE 1.3500 TO #FATOR`.
> Em arrays, o intervalo faz parte da notação: `(A60/1:10)`, `(N3.4/1:27)`, `(N3.6/1:10,1:12)`.

Blocos importantes:

| Bloco | Finalidade |
|-------|---------|
| `DEFINE DATA LOCAL` | Declarações de variáveis no escopo deste programa |
| `DEFINE DATA PARAMETER` | Variáveis de entrada/saída recebidas de um chamador |
| `DEFINE DATA GLOBAL` | Compartilhadas entre programas em uma sessão (raro e frágil) |
| `INPUT` | Lê do terminal (online) ou de arquivo sequencial (batch) |
| `DISPLAY` / `WRITE` | Saída para tela ou relatório |
| `MAP` | Definição do layout da tela (IU de terminal) |

## CALLNAT e PERFORM

- **`CALLNAT 'SUBPROG' parm1 parm2`**: chama um subprograma externo (arquivo-fonte separado). Os parâmetros são passados por referência, salvo quando marcados `(AD=O)` somente para saída.
- **`PERFORM subroutine-name`**: chama uma sub-rotina interna definida com `DEFINE SUBROUTINE ... END-SUBROUTINE` no mesmo programa.

Ao mapear cadeias de chamadas, `CALLNAT` é essencial porque cruza limites de arquivos.

## Copycodes INCLUDE

`INCLUDE copycode-name` insere um fragmento de código compartilhado durante a compilação, como `#include` em C. Copycodes geralmente contêm:

- Definições de áreas de dados compartilhadas (a "struct" do Natural)
- Rotinas comuns de validação
- Blocos padrão de tratamento de erros

Ao encontrar `INCLUDE`, localize o copycode correspondente para entender o layout completo dos dados.

### Extensões de membros

Uma biblioteca Natural é **plana**: não há subdiretórios, e cada membro é resolvido pelo nome, não pelo path. A extensão indica o tipo:

| Extensão | Tipo | Chamado por |
|----------|------|-------------|
| `.NSN` | Programa ou subprograma | executado por JCL ou `CALLNAT` |
| `.NSA` | Parameter Data Area (PDA) | `PARAMETER USING` |
| `.NSL` | Local Data Area (LDA) | `LOCAL USING` |
| `.NSC` | Copycode | `INCLUDE` |
| `.NSM` | Map (layout de tela 3270) | `INPUT USING MAP` |
| `.jcl` | Job Control Language | agendador batch |

`CALLNAT`, `INCLUDE`, `PARAMETER USING` e `LOCAL USING` **NÃO DEVEM ser ignorados**: cada um incorpora código ou declarações de outro arquivo. A leitura isolada de um programa é incompleta.

Os nomes de membros Natural são limitados a 8 caracteres. Neste corpus, os nomes dos DDMs/membros Natural são `BENEFIC`, `SOCPROG`, `PAYMENT` e `AUDIT`. O arquivo Adabas ainda pode ser descrito conceitualmente como arquivo de Beneficiário ou Programa Social, e os nomes dos campos DDM mantêm seus nomes longos.

## FDT Adabas (Field Definition Table)

Todo arquivo Adabas possui uma FDT que define seus campos. Considere-a o schema:

| Coluna | Significado |
|--------|---------|
| Nível | Profundidade hierárquica (01 = nível superior, 02+ = filhos) |
| Nome | Nome curto de dois caracteres (AA, AB, AC...) |
| Formato | `A` = alfabético, `N` = numérico, `P` = compactado, `B` = binário, `D` = data, `T` = hora |
| Tamanho | Tamanho do campo em bytes |
| Descritor | `DE` = índice pesquisável, `MU` = vários valores (array), `PE` = grupo periódico (repetido) |

### Campos MU (múltiplos valores)

Um campo marcado como `MU` pode conter vários valores (como um array). No Natural, ele é acessado por índice: `FIELD(1)`, `FIELD(2)` etc. A FDT define a quantidade máxima de ocorrências.

**Mapeamento moderno**: `@ElementCollection` em JPA ou uma coluna JSONB no PostgreSQL.

### PE (grupos periódicos)

Um grupo `PE` é um grupo repetido de campos relacionados, como uma linha em uma tabela incorporada. Por exemplo, um histórico de endereços em que cada ocorrência possui rua, cidade e data.

**Mapeamento moderno**: relacionamento `@OneToMany` com entidade incorporada ou array JSONB.

### Superdescritores

Um superdescritor combina vários campos em uma única chave pesquisável (índice composto). Uma notação como `SU = AA + AB(1-4)` significa "concatenar o campo AA com os 4 primeiros bytes de AB".

**Mapeamento moderno**: `@Index(columnList = "col_a, col_b")` em JPA.

## Convenções de nomenclatura dos anos 1990

Bases de código Natural legadas usam nomes baseados em prefixos. Padrões comuns:

| Padrão de prefixo | Significado típico |
|---|---|
| `BN-` ou `BATCH-` | Programa batch ou variável relacionada a batch |
| `PG-` ou `PROG-` | Programa principal |
| `PS-` ou `SUB-` | Subprograma (chamado por CALLNAT) |
| `AU-` ou `AUT-` | Relacionado a autorização ou auditoria |
| Prefixo `#` em variáveis | Variável de trabalho local (convenção Natural) |
| Prefixo `+` em variáveis | Variável de parâmetro passada pelo chamador |

Essas são convenções, não regras; verifique no código em vez de presumir.

## Padrões de jobs batch

Programas Natural batch geralmente seguem esta estrutura:

```
READ WORK FILE 1 record
  /* processa cada registro */
  AT END OF DATA
    /* totais finais / limpeza */
  END-ENDDATA
END-WORK
```

Relatórios de quebra de controle usam:

```
READ logical-file BY descriptor
  AT BREAK OF descriptor
    /* subtotal quando o valor do descritor muda */
  BEFORE BREAK PROCESSING
    /* linha de detalhe de cada registro */
  END-BREAK
END-READ
```

## Tratamento de decimal compactado

O decimal compactado (formato `P`) armazena dígitos com eficiência: cada byte contém dois dígitos, e o nibble final é o sinal (C=positivo, D=negativo). Ele é comum em cálculos financeiros.

Ao mapear para Java, SEMPRE use `BigDecimal`, NUNCA `double` ou `float`. Campos compactados no formato `P9.2` significam 9 dígitos inteiros mais 2 casas decimais → `BigDecimal` com `scale(2)`.

**No mainframe, valores monetários são compactados (`P`), não `N`.** Ao ler o corpus, um valor monetário declarado como `N` é um alerta: pode ser um descuido da autoria original ou uma divergência deliberada entre o programa e o DDM. SEMPRE compare o formato no programa com o formato do mesmo campo no `.ddm`: divergências de tipo e tamanho são uma fonte clássica de truncamento silencioso e overflow.

## Estratégia de leitura

Ao abordar um programa legado pela primeira vez:

1. **Comece com DEFINE DATA**: entenda as variáveis e seus tipos
2. **Encontre o READ ou FIND principal**: ele revela quais dados o programa processa
3. **Rastreie chamadas CALLNAT**: elas são as dependências
4. **Procure copycodes INCLUDE**: eles ampliam as definições de dados
5. **Verifique AT BREAK / AT END OF DATA**: revelam a lógica de relatório ou processamento
6. **Registre todo ESCAPE ou ON ERROR**: são caminhos de tratamento de erros
7. **Verifique `IF NO RECORDS FOUND`**: o bloco `FIND ... IF NO RECORDS FOUND ... END-NOREC` define o que ocorre quando a busca não retorna nada; padrões silenciosos ficam ocultos aqui. Campos da view possuem valores somente **dentro** do bloco `FIND`/`READ`.
8. **Compare `FIND ... WITH` com o DDM**: buscas só são possíveis em campos marcados como descritores (`D`, `S` ou `H`) na listagem DDM. Uma busca em campo sem descritor não compila.

## Convenções

| Regra | Justificativa |
|---|---|
| Neste laboratório, declarações Natural usam notação decimal com ponto, como `(P9.2)` | A notação com vírgula, como `(P9,2)`, falha com `NAT0165` no Natural CE 9.3.3 |
| Rastreie `CALLNAT`, `INCLUDE`, `PARAMETER USING` e `LOCAL USING` | Um membro Natural lido isoladamente está incompleto |
| Compare os formatos dos campos do programa com o DDM correspondente | Divergências de tipo e tamanho podem causar truncamento silencioso ou overflow |
| Mapeie campos monetários compactados para `BigDecimal` | `double` e `float` perdem precisão financeira |
| Verifique descritores antes de interpretar `FIND ... WITH` | As buscas compilam somente em campos descritores no DDM |
| Trate prefixos como indícios, não provas | As convenções legadas variam e devem ser verificadas no código |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Comece com `DEFINE DATA` para entender variáveis e tipos | Interprete regras de negócio antes de conhecer o layout dos dados |
| Encontre o `READ` ou `FIND` principal para identificar os dados processados | Presuma o arquivo principal somente pelo nome do programa |
| Rastreie toda dependência `CALLNAT` e copycode `INCLUDE` | Ignore subprogramas externos, PDAs, LDAs, copycodes ou maps |
| Verifique os caminhos `AT BREAK`, `AT END OF DATA`, `ESCAPE` e `ON ERROR` | Leia somente o caminho feliz do programa |
| Verifique `IF NO RECORDS FOUND` e o escopo dos campos de view nos blocos `FIND`/`READ` | Presuma que registros ausentes e campos de view se comportam como variáveis normais |
| Compare `FIND ... WITH` com os descritores DDM | Presuma que um campo sem descritor pode ser pesquisado |

## Lista de verificação antes de abrir uma PR

- [ ] Variáveis, arrays, parâmetros e formatos pertinentes de `DEFINE DATA` foram registrados antes do resumo do comportamento
- [ ] Os caminhos principais de `READ`, `FIND`, arquivo de trabalho, relatório e quebra de controle foram identificados
- [ ] Toda dependência `CALLNAT`, `INCLUDE`, `PARAMETER USING`, `LOCAL USING`, map e JCL foi rastreada ou registrada como aberta
- [ ] Os formatos de campos do programa foram comparados com o DDM quanto a tipo, tamanho, descritor, MU, PE e superdescritor
- [ ] Valores decimais compactados e monetários foram mapeados ou documentados como candidatos a `BigDecimal`, nunca como ponto flutuante
- [ ] Caminhos de erro, escape, ausência de registros, fim dos dados e padrões silenciosos foram incluídos nas regras de negócio extraídas
