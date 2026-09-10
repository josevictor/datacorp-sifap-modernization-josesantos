---
name: "copilot-sdk"
description: "Crie aplicações agênticas com o GitHub Copilot SDK. Use ao incorporar agentes de IA em aplicações, criar ferramentas personalizadas, implementar respostas em transmissão contínua, gerenciar sessões, conectar-se a servidores MCP ou criar agentes personalizados. Os gatilhos incluem Copilot SDK, GitHub SDK, aplicação agêntica, incorporar Copilot, agente programável, servidor MCP e agente personalizado."
---
# GitHub Copilot SDK

Incorpore os fluxos de trabalho agênticos do Copilot a qualquer aplicação com Python, TypeScript, Go ou .NET.

| Área | Seções |
|---|---|
| Configuração | Pré-requisitos, instalação, início rápido |
| Interação | Respostas em transmissão contínua, assistente interativo de CLI, padrões comuns |
| Extensão do agente | Ferramentas personalizadas, integração com servidor MCP, agentes personalizados, mensagem do sistema |
| Configuração avançada | Configuração do cliente, configuração da sessão, persistência da sessão |
| Referência | Tipos de evento, modelos disponíveis, práticas recomendadas, arquitetura |

## Visão geral

O GitHub Copilot SDK expõe o mesmo mecanismo da CLI do Copilot: um ambiente de execução de agentes testado em produção que você pode invocar por código. Não é necessário criar sua própria orquestração. Você define o comportamento do agente, e o Copilot cuida do planejamento, da invocação de ferramentas, da edição de arquivos e de outras tarefas.

## Quando usar

- "Incorpore um agente do Copilot à nossa aplicação com o Copilot SDK."
- "Adicione uma ferramenta personalizada que o agente possa chamar durante uma sessão."
- "Transmita continuamente a resposta do modelo, token por token, em nossa CLI."
- "Conecte o SDK a um servidor MCP e a um agente personalizado."

> [!NOTE]
> O SDK controla a GitHub Copilot CLI, que deve estar instalada e autenticada (consulte os pré-requisitos). Ele está em versão prévia técnica (Technical Preview) e pode introduzir alterações incompatíveis. Fixe as versões e teste novamente ao atualizar.

## Pré-requisitos

1. **GitHub Copilot CLI** instalada e autenticada ([guia de instalação](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli))
2. **Ambiente de execução da linguagem**: Node.js 18+, Python 3.8+, Go 1.21+ ou .NET 8.0+

Verifique a CLI: `copilot --version`

## Instalação

### Node.js/TypeScript

```bash
mkdir copilot-demo && cd copilot-demo
npm init -y --init-type module
npm install @github/copilot-sdk tsx
```

### Instalação para Python

```bash
pip install github-copilot-sdk
```

### Instalação para Go

```bash
mkdir copilot-demo && cd copilot-demo
go mod init copilot-demo
go get github.com/github/copilot-sdk/go
```

### Instalação para .NET

```bash
dotnet new console -n CopilotDemo && cd CopilotDemo
dotnet add package GitHub.Copilot.SDK
```

## Início rápido

### Início rápido com TypeScript

```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
});

const response = await session.sendAndWait({ prompt: "Quanto é 2 + 2?" });
console.log(response?.data.content);

await client.stop();
process.exit(0);
```

Execute: `npx tsx index.ts`

### Início rápido com Python

```python
import asyncio
from copilot import CopilotClient, PermissionHandler

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
    })
    response = await session.send_and_wait({"prompt": "Quanto é 2 + 2?"})

    print(response.data.content)
    await client.stop()

asyncio.run(main())
```

### Início rápido com Go

```go
package main

import (
    "fmt"
    "log"
    "os"
    copilot "github.com/github/copilot-sdk/go"
)

func main() {
    client := copilot.NewClient(nil)
    if err := client.Start(); err != nil {
        log.Fatal(err)
    }
    defer client.Stop()

    session, err := client.CreateSession(&copilot.SessionConfig{
        OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
        Model:               "gpt-4.1",
    })
    if err != nil {
        log.Fatal(err)
    }

    response, err := session.SendAndWait(copilot.MessageOptions{Prompt: "Quanto é 2 + 2?"}, 0)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println(*response.Data.Content)
    os.Exit(0)
}
```

### .NET (C#)

```csharp
using GitHub.Copilot.SDK;

await using var client = new CopilotClient();
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
});

var response = await session.SendAndWaitAsync(new MessageOptions { Prompt = "Quanto é 2 + 2?" });
Console.WriteLine(response?.Data.Content);
```

Execute: `dotnet run`

## Respostas em transmissão contínua

Ative a saída em tempo real para melhorar a experiência de uso:

### Respostas em transmissão contínua com TypeScript

```typescript
import { CopilotClient, approveAll, SessionEvent } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    streaming: true,
});

session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
    }
    if (event.type === "session.idle") {
        console.log(); // Nova linha ao concluir
    }
});

await session.sendAndWait({ prompt: "Conte uma piada curta" });

await client.stop();
process.exit(0);
```

### Respostas em transmissão contínua com Python

```python
import asyncio
import sys
from copilot import CopilotClient, PermissionHandler
from copilot.generated.session_events import SessionEventType

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
        "streaming": True,
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()
        if event.type == SessionEventType.SESSION_IDLE:
            print()

    session.on(handle_event)
    await session.send_and_wait({"prompt": "Conte uma piada curta"})
    await client.stop()

asyncio.run(main())
```

### Respostas em transmissão contínua com Go

```go
session, err := client.CreateSession(&copilot.SessionConfig{
 OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
    Model:     "gpt-4.1",
    Streaming: true,
})

session.On(func(event copilot.SessionEvent) {
    if event.Type == "assistant.message_delta" {
        fmt.Print(*event.Data.DeltaContent)
    }
    if event.Type == "session.idle" {
        fmt.Println()
    }
})

_, err = session.SendAndWait(copilot.MessageOptions{Prompt: "Conte uma piada curta"}, 0)
```

### Respostas em transmissão contínua com .NET

```csharp
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
    Streaming = true,
});

session.On(ev =>
{
    if (ev is AssistantMessageDeltaEvent deltaEvent)
        Console.Write(deltaEvent.Data.DeltaContent);
    if (ev is SessionIdleEvent)
        Console.WriteLine();
});

await session.SendAndWaitAsync(new MessageOptions { Prompt = "Conte uma piada curta" });
```

## Ferramentas personalizadas

Defina ferramentas que o Copilot pode invocar durante o raciocínio. Ao definir uma ferramenta, você informa ao Copilot:

1. **O que a ferramenta faz** (descrição)
2. **Quais parâmetros ela requer** (esquema)
3. **Qual código executar** (manipulador)

### TypeScript (JSON Schema, esquema JSON)

```typescript
import { CopilotClient, approveAll, defineTool, SessionEvent } from "@github/copilot-sdk";

const getWeather = defineTool("get_weather", {
    description: "Obtenha o clima atual de uma cidade",
    parameters: {
        type: "object",
        properties: {
            city: { type: "string", description: "O nome da cidade" },
        },
        required: ["city"],
    },
    handler: async (args: { city: string }) => {
        const { city } = args;
        // Em uma aplicação real, chame uma API de clima aqui
        const conditions = ["ensolarado", "nublado", "chuvoso", "parcialmente nublado"];
        const temp = Math.floor(Math.random() * 30) + 50;
        const condition = conditions[Math.floor(Math.random() * conditions.length)];
        return { city, temperature: `${temp}°F`, condition };
    },
});

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    streaming: true,
    tools: [getWeather],
});

session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
    }
});

await session.sendAndWait({
    prompt: "Como está o clima em Seattle e Tóquio?",
});

await client.stop();
process.exit(0);
```

### Python (Pydantic)

```python
import asyncio
import random
import sys
from copilot import CopilotClient, PermissionHandler
from copilot.tools import define_tool
from copilot.generated.session_events import SessionEventType
from pydantic import BaseModel, Field

class GetWeatherParams(BaseModel):
    city: str = Field(description="O nome da cidade cuja previsão será consultada")

@define_tool(description="Obtenha o clima atual de uma cidade")
async def get_weather(params: GetWeatherParams) -> dict:
    city = params.city
    conditions = ["ensolarado", "nublado", "chuvoso", "parcialmente nublado"]
    temp = random.randint(50, 80)
    condition = random.choice(conditions)
    return {"city": city, "temperature": f"{temp}°F", "condition": condition}

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
        "streaming": True,
        "tools": [get_weather],
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()

    session.on(handle_event)

    await session.send_and_wait({
        "prompt": "Como está o clima em Seattle e Tóquio?"
    })

    await client.stop()

asyncio.run(main())
```

### Ferramentas personalizadas com Go

```go
type WeatherParams struct {
    City string `json:"city" jsonschema:"O nome da cidade"`
}

type WeatherResult struct {
    City        string `json:"city"`
    Temperature string `json:"temperature"`
    Condition   string `json:"condition"`
}

getWeather := copilot.DefineTool(
    "get_weather",
    "Obtenha o clima atual de uma cidade",
    func(params WeatherParams, inv copilot.ToolInvocation) (WeatherResult, error) {
        conditions := []string{"ensolarado", "nublado", "chuvoso", "parcialmente nublado"}
        temp := rand.Intn(30) + 50
        condition := conditions[rand.Intn(len(conditions))]
        return WeatherResult{
            City:        params.City,
            Temperature: fmt.Sprintf("%d°F", temp),
            Condition:   condition,
        }, nil
    },
)

session, _ := client.CreateSession(&copilot.SessionConfig{
 OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
    Model:     "gpt-4.1",
    Streaming: true,
    Tools:     []copilot.Tool{getWeather},
})
```

### .NET (Microsoft.Extensions.AI)

```csharp
using GitHub.Copilot.SDK;
using Microsoft.Extensions.AI;
using System.ComponentModel;

var getWeather = AIFunctionFactory.Create(
    ([Description("O nome da cidade")] string city) =>
    {
        var conditions = new[] { "ensolarado", "nublado", "chuvoso", "parcialmente nublado" };
        var temp = Random.Shared.Next(50, 80);
        var condition = conditions[Random.Shared.Next(conditions.Length)];
        return new { city, temperature = $"{temp}°F", condition };
    },
    "get_weather",
    "Obtenha o clima atual de uma cidade"
);

await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
    Streaming = true,
    Tools = [getWeather],
});
```

## Como as ferramentas funcionam

Quando o Copilot decide chamar sua ferramenta:

1. O Copilot envia uma solicitação de chamada de ferramenta com os parâmetros.
2. O SDK executa sua função manipuladora.
3. O resultado é enviado de volta ao Copilot.
4. O Copilot incorpora o resultado à resposta.

O Copilot decide quando chamar a ferramenta com base na pergunta da pessoa e na descrição da ferramenta.

## Assistente interativo de CLI

Crie um assistente interativo completo:

### Assistente interativo de CLI com TypeScript

```typescript
import { CopilotClient, approveAll, defineTool, SessionEvent } from "@github/copilot-sdk";
import * as readline from "readline";

const getWeather = defineTool("get_weather", {
    description: "Obtenha o clima atual de uma cidade",
    parameters: {
        type: "object",
        properties: {
            city: { type: "string", description: "O nome da cidade" },
        },
        required: ["city"],
    },
    handler: async ({ city }) => {
        const conditions = ["ensolarado", "nublado", "chuvoso", "parcialmente nublado"];
        const temp = Math.floor(Math.random() * 30) + 50;
        const condition = conditions[Math.floor(Math.random() * conditions.length)];
        return { city, temperature: `${temp}°F`, condition };
    },
});

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    streaming: true,
    tools: [getWeather],
});

session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
    }
});

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

console.log("Assistente de clima (digite 'sair' para encerrar)");
console.log("Experimente: 'Como está o clima em Paris?'\n");

const prompt = () => {
    rl.question("Você: ", async (input) => {
        if (input.toLowerCase() === "sair") {
            await client.stop();
            rl.close();
            return;
        }

        process.stdout.write("Assistente: ");
        await session.sendAndWait({ prompt: input });
        console.log("\n");
        prompt();
    });
};

prompt();
```

### Assistente interativo de CLI com Python

```python
import asyncio
import random
import sys
from copilot import CopilotClient, PermissionHandler
from copilot.tools import define_tool
from copilot.generated.session_events import SessionEventType
from pydantic import BaseModel, Field

class GetWeatherParams(BaseModel):
    city: str = Field(description="O nome da cidade cuja previsão será consultada")

@define_tool(description="Obtenha o clima atual de uma cidade")
async def get_weather(params: GetWeatherParams) -> dict:
    conditions = ["ensolarado", "nublado", "chuvoso", "parcialmente nublado"]
    temp = random.randint(50, 80)
    condition = random.choice(conditions)
    return {"city": params.city, "temperature": f"{temp}°F", "condition": condition}

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
        "streaming": True,
        "tools": [get_weather],
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()

    session.on(handle_event)

    print("Assistente de clima (digite 'sair' para encerrar)")
    print("Experimente: 'Como está o clima em Paris?'\n")

    while True:
        try:
            user_input = input("Você: ")
        except EOFError:
            break

        if user_input.lower() == "sair":
            break

        sys.stdout.write("Assistente: ")
        await session.send_and_wait({"prompt": user_input})
        print("\n")

    await client.stop()

asyncio.run(main())
```

## Integração com servidor MCP

Conecte-se a servidores MCP (Model Context Protocol) para usar ferramentas prontas. Conecte-se ao servidor MCP do GitHub para acessar repositórios, issues e PRs:

### Integração com servidor MCP em TypeScript

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    mcpServers: {
        github: {
            type: "http",
            url: "https://api.githubcopilot.com/mcp/",
        },
    },
});
```

### Integração com servidor MCP em Python

```python
session = await client.create_session({
    "on_permission_request": PermissionHandler.approve_all,
    "model": "gpt-4.1",
    "mcp_servers": {
        "github": {
            "type": "http",
            "url": "https://api.githubcopilot.com/mcp/",
        },
    },
})
```

### Integração com servidor MCP em Go

```go
session, _ := client.CreateSession(&copilot.SessionConfig{
 OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
    Model: "gpt-4.1",
    MCPServers: map[string]copilot.MCPServerConfig{
        "github": {
            "type": "http",
            "url": "https://api.githubcopilot.com/mcp/",
        },
    },
})
```

### Integração com servidor MCP em .NET

```csharp
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
    McpServers = new Dictionary<string, McpServerConfig>
    {
        ["github"] = new McpServerConfig
        {
            Type = "http",
            Url = "https://api.githubcopilot.com/mcp/",
        },
    },
});
```

## Agentes personalizados

Defina personas especializadas de IA para tarefas específicas:

### Agentes personalizados em TypeScript

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    customAgents: [{
        name: "pr-reviewer",
        displayName: "Revisor de PR",
        description: "Revisa pull requests conforme as práticas recomendadas",
        prompt: "Você é especialista em revisão de código. Concentre-se em segurança, desempenho e manutenibilidade.",
    }],
});
```

### Agentes personalizados em Python

```python
session = await client.create_session({
    "on_permission_request": PermissionHandler.approve_all,
    "model": "gpt-4.1",
    "custom_agents": [{
        "name": "pr-reviewer",
        "display_name": "Revisor de PR",
        "description": "Revisa pull requests conforme as práticas recomendadas",
        "prompt": "Você é especialista em revisão de código. Concentre-se em segurança, desempenho e manutenibilidade.",
    }],
})
```

## Mensagem do sistema

Personalize o comportamento e a personalidade da IA:

### Mensagem do sistema em TypeScript

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    systemMessage: {
        content: "Você é um assistente prestativo para nossa equipe de engenharia. Seja sempre conciso.",
    },
});
```

### Mensagem do sistema em Python

```python
session = await client.create_session({
    "on_permission_request": PermissionHandler.approve_all,
    "model": "gpt-4.1",
    "system_message": {
        "content": "Você é um assistente prestativo para nossa equipe de engenharia. Seja sempre conciso.",
    },
})
```

## Servidor externo da CLI

Execute a CLI separadamente no modo de servidor e conecte o SDK a ela. Isso é útil para depuração, compartilhamento de recursos ou ambientes personalizados.

### Iniciar a CLI no modo de servidor

```bash
copilot --server --port 4321
```

### Conectar o SDK a um servidor externo

#### Conectar o SDK a um servidor externo com TypeScript

```typescript
const client = new CopilotClient({
    cliUrl: "localhost:4321"
});

const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
});
```

#### Conectar o SDK a um servidor externo com Python

```python
client = CopilotClient({
    "cli_url": "localhost:4321"
})
await client.start()

session = await client.create_session({
    "on_permission_request": PermissionHandler.approve_all,
    "model": "gpt-4.1",
})
```

#### Conectar o SDK a um servidor externo com Go

```go
client := copilot.NewClient(&copilot.ClientOptions{
    CLIUrl: "localhost:4321",
})

if err := client.Start(); err != nil {
    log.Fatal(err)
}

session, _ := client.CreateSession(&copilot.SessionConfig{
 OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
 Model:               "gpt-4.1",
})
```

#### Conectar o SDK a um servidor externo com .NET

```csharp
using var client = new CopilotClient(new CopilotClientOptions
{
    CliUrl = "localhost:4321"
});

await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
});
```

**Observação:** quando `cliUrl` é fornecida, o SDK não inicia nem gerencia um processo da CLI. Ele apenas se conecta ao servidor existente.

## Tipos de evento

| Evento | Descrição |
|-------|-------------|
| `user.message` | Entrada da pessoa adicionada |
| `assistant.message` | Resposta completa do modelo |
| `assistant.message_delta` | Trecho da resposta em transmissão contínua |
| `assistant.reasoning` | Raciocínio do modelo (depende do modelo) |
| `assistant.reasoning_delta` | Trecho do raciocínio em transmissão contínua |
| `tool.execution_start` | Invocação da ferramenta iniciada |
| `tool.execution_complete` | Execução da ferramenta concluída |
| `session.idle` | Nenhum processamento ativo |
| `session.error` | Ocorreu um erro |

## Configuração do cliente

| Opção | Descrição | Padrão |
|--------|-------------|---------|
| `cliPath` | Caminho do executável da Copilot CLI | PATH do sistema |
| `cliUrl` | Conexão com servidor existente (por exemplo, "localhost:4321") | Nenhum |
| `port` | Porta de comunicação do servidor | Aleatória |
| `useStdio` | Uso do transporte stdio em vez de TCP | true |
| `logLevel` | Detalhamento dos registros | "info" |
| `autoStart` | Inicialização automática do servidor | true |
| `autoRestart` | Reinicialização após falhas | true |
| `cwd` | Diretório de trabalho do processo da CLI | Herdado |

## Configuração da sessão

| Opção | Descrição |
|--------|-------------|
| `model` | LLM a usar ("gpt-4.1", "claude-sonnet-4.5" etc.) |
| `sessionId` | Identificador personalizado da sessão |
| `tools` | Definições de ferramentas personalizadas |
| `mcpServers` | Conexões com servidores MCP |
| `customAgents` | Personas de agentes personalizados |
| `systemMessage` | Substituição da instrução padrão do sistema |
| `streaming` | Ativação de trechos incrementais da resposta |
| `availableTools` | Lista de ferramentas permitidas |
| `excludedTools` | Lista de ferramentas desativadas |

## Persistência da sessão

Salve e retome conversas após reinicializações:

### Criar com ID personalizado

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    sessionId: "user-123-conversation",
    model: "gpt-4.1"
});
```

### Retomar sessão

```typescript
const session = await client.resumeSession("user-123-conversation", { onPermissionRequest: approveAll });
await session.send({ prompt: "O que discutimos anteriormente?" });
```

### Listar e excluir sessões

```typescript
const sessions = await client.listSessions();
await client.deleteSession("old-session-id");
```

## Tratamento de erros

```typescript
try {
    const client = new CopilotClient();
    const session = await client.createSession({
        onPermissionRequest: approveAll,
        model: "gpt-4.1",
    });
    const response = await session.sendAndWait(
        { prompt: "Olá!" },
        30000 // tempo limite em ms
    );
} catch (error) {
    if (error.code === "ENOENT") {
        console.error("A Copilot CLI não está instalada");
    } else if (error.code === "ECONNREFUSED") {
        console.error("Não foi possível conectar ao servidor do Copilot");
    } else {
        console.error("Erro:", error.message);
    }
} finally {
    await client.stop();
}
```

## Encerramento controlado

```typescript
process.on("SIGINT", async () => {
    console.log("Encerrando...");
    await client.stop();
    process.exit(0);
});
```

## Padrões comuns

### Conversa em vários turnos

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
});

await session.sendAndWait({ prompt: "Meu nome é Alice" });
await session.sendAndWait({ prompt: "Qual é o meu nome?" });
// Resposta: "Seu nome é Alice"
```

### Anexos de arquivo

```typescript
await session.send({
    prompt: "Analise este arquivo",
    attachments: [{
        type: "file",
        path: "./data.csv",
        displayName: "Dados de vendas"
    }]
});
```

### Interromper operações longas

```typescript
const timeoutId = setTimeout(() => {
    session.abort();
}, 60000);

session.on((event) => {
    if (event.type === "session.idle") {
        clearTimeout(timeoutId);
    }
});
```

## Modelos disponíveis

Consulte os modelos disponíveis durante a execução:

```typescript
const models = await client.getModels();
// Retorna: ["gpt-4.1", "gpt-4o", "claude-sonnet-4.5", ...]
```

## Práticas recomendadas

1. **Sempre faça a limpeza**: use `try-finally` ou `defer` para garantir a chamada de `client.stop()`.
2. **Defina tempos limite**: use `sendAndWait` com tempo limite para operações longas.
3. **Trate eventos**: assine eventos de erro para ter um tratamento de erros robusto.
4. **Use transmissão contínua**: ative a transmissão contínua para melhorar a experiência em respostas longas.
5. **Persista as sessões**: use IDs personalizados para conversas em vários turnos.
6. **Defina ferramentas claras**: escreva nomes e descrições elucidativos para as ferramentas.

## Arquitetura

```text
Sua aplicação
       |
  Cliente SDK
       | JSON-RPC
  Copilot CLI (modo de servidor)
       |
  GitHub (modelos, autenticação)
```

O SDK gerencia automaticamente o ciclo de vida do processo da CLI. Toda comunicação ocorre por JSON-RPC sobre stdio ou TCP.

## Modelo de saída

Uma integração entregue segue esta estrutura: cliente, sessão, ferramentas opcionais, loop de execução e limpeza garantida:

```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

// 1. Crie o cliente e uma sessão (adicione ferramentas personalizadas por `tools: [...]`).
const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    streaming: true,
});

// 2. Controle o agente.
try {
    const response = await session.sendAndWait({ prompt: "..." }, 30000);
    console.log(response?.data.content);
} finally {
    // 3. Sempre faça a limpeza.
    await client.stop();
}
```

Informe a linguagem e o ambiente de execução, os modelos usados, as ferramentas ou os servidores MCP conectados e como o processo é limpo.

## Critérios de qualidade

- [ ] A Copilot CLI está instalada e autenticada, e o ambiente de execução escolhido corresponde ao SDK (Node.js 18+, Python 3.8+, Go 1.21+ ou .NET 8.0+).
- [ ] `client.stop()` está garantido em todos os caminhos (`try/finally`, `defer` ou `await using`).
- [ ] Chamadas longas usam `sendAndWait` com tempo limite, e os erros e eventos `session.error` são tratados.
- [ ] As ferramentas personalizadas declaram nome, descrição e esquema de parâmetros claros.
- [ ] Segredos e tokens nunca são fixados no código. Pontos de extremidade MCP e modelos permanecem na configuração.
- [ ] A integração é executada de ponta a ponta no modelo de destino antes de ser considerada concluída.

## Recursos

- **Repositório do GitHub**: https://github.com/github/copilot-sdk
- **Tutorial de introdução**: https://github.com/github/copilot-sdk/blob/main/docs/tutorials/first-app.md
- **Servidor MCP do GitHub**: https://github.com/github/github-mcp-server
- **Diretório de servidores MCP**: https://github.com/modelcontextprotocol/servers
- **Livro de receitas**: https://github.com/github/copilot-sdk/tree/main/cookbook
- **Exemplos**: https://github.com/github/copilot-sdk/tree/main/samples

## Status

Este SDK está em **versão prévia técnica (Technical Preview)** e pode receber alterações incompatíveis. Ainda não é recomendado para uso em produção.
