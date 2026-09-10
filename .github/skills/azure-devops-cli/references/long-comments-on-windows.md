# Publicação de comentários e corpos longos no Windows

No Windows, o comando `az` é resolvido como `az.cmd`, um programa intermediário em lote invocado pelo `cmd.exe`. A linha de comando completa tem um limite de cerca de 8.191 caracteres. Portanto, um valor longo de `--discussion`, `--description` ou `--content` pode ser truncado silenciosamente ou falhar. Detecte o interpretador de comandos antes de compor um argumento longo e escolha a abordagem adequada. Ignorar isso é o motivo mais comum para o agente gastar de 3 a 5 interações recorrendo à obtenção direta de tokens e a chamadas REST.

## Detecte primeiro o interpretador de comandos

| Ambiente | Sinal | Ação |
|---|---|---|
| PowerShell no Windows | `$IsWindows -eq $true` e `$PSVersionTable.PSVersion` definido | Use `azps.ps1` (veja abaixo) |
| PowerShell no macOS/Linux | `$IsWindows -eq $false` | O `az` comum funciona, sem o programa intermediário do cmd.exe |
| bash/zsh/sh | `$BASH_VERSION` ou `$ZSH_VERSION` definido, ou `uname` funciona | O `az` comum funciona, sem o programa intermediário do cmd.exe |
| `cmd.exe` do Windows | `%ComSpec%` termina em `cmd.exe`, sem `$PSVersionTable` | Use `azps.ps1` se o PowerShell estiver instalado. Caso contrário, veja a alternativa com `az devops invoke` abaixo |

## Opção 1: `azps.ps1` (PowerShell no Windows)

O `azps.ps1` acompanha o instalador da CLI do Azure e invoca diretamente o ponto de entrada Python. Não há o limite de comprimento do `cmd.exe`.

```powershell
# Leia o corpo longo em uma variável e forneça-o diretamente. Sem problemas com aspas.
$body = Get-Content -Raw .\comment.md
azps.ps1 boards work-item update --id 1234 --discussion $body
```

## Opção 2: opção dedicada `--file-path` quando oferecida pela CLI do Azure

Alguns comandos têm uma opção nativa de arquivo. Prefira-a a qualquer corpo embutido:

- `az devops wiki page create` e `az devops wiki page update` aceitam `--file-path` (com `--encoding` opcional).
- Use-a em qualquer interpretador de comandos, inclusive no Windows.

```bash
az devops wiki page create --path 'My page' --wiki myproject --file-path ./page.md --encoding utf-8
```

## Opção 3: alternativa com `az devops invoke`

Quando não houver `--file-path` (`--discussion` de item de trabalho, `--description` de solicitação de pull) e você não estiver no PowerShell, publique o corpo pela API REST subjacente. O `az devops invoke` é executado no ponto de entrada Python, portanto também não está sujeito ao limite do `cmd.exe`, e lê o corpo da solicitação de um arquivo com `--in-file`:

```bash
# Publique um comentário de discussão longo no item de trabalho 1234.
# REST: POST /{project}/_apis/wit/workItems/{id}/comments?api-version=7.0-preview.3
az devops invoke \
  --area wit --resource comments \
  --route-parameters project={project} workItemId=1234 \
  --api-version 7.0-preview.3 \
  --http-method POST \
  --in-file ./comment.json
```

Nesse caso, `comment.json` é `{ "text": "<long markdown body>" }`. Esta é a solução universal quando nem `azps.ps1` nem `--file-path` estão disponíveis. O próprio `az devops invoke` aceita `--in-file` nativamente.

## Não dependa de `@<file>` para argumentos de texto simples

A convenção `@<file>` da CLI do Azure está documentada para parâmetros JSON (consulte o [guia oficial sobre aspas](https://learn.microsoft.com/en-us/cli/azure/use-azure-cli-successfully-quoting)). Não há garantia de que ela expanda argumentos de texto simples como `--discussion` ou `--description`. Portanto, não a use como substituta das três opções acima.
