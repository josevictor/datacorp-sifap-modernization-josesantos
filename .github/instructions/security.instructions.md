---
description: "Use ao implementar ou revisar autenticação, autorização, criptografia, configuração segura, tratamento de segredos e código sensível à segurança."
applyTo: "backend/src/main/java/**/auth/**,backend/src/main/java/**/security/**,backend/src/main/java/**/config/**,backend/src/main/resources/**,frontend/**/auth/**,frontend/**/middleware.ts"
---

# Convenções de segurança — Autenticação, segredos e injeção

Este arquivo é ativado em código sensível à segurança: pacotes `auth/`, `security/` e `config/`, tudo em `backend/src/main/resources/`, além de `frontend/**/auth/**` e `frontend/middleware.ts`. Ele ensina autenticação, autorização, validação de entrada, CORS, tratamento de segredos e proteção de dados sensíveis conforme as regras OWASP Top 10 do repositório. O formato REST geral fica em [`backend.instructions.md`](backend.instructions.md); o armazenamento de segredos no Terraform fica em [`infrastructure.instructions.md`](infrastructure.instructions.md).

## Autenticação (OAuth2 / JWT)

O backend é um resource server OAuth2 sem estado que valida JWTs pelo Spring Security. Nunca implemente manualmente a análise de tokens nem a criptografia.

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health").permitAll()
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth -> oauth.jwt(Customizer.withDefaults()))
            .cors(Customizer.withDefaults())
            .csrf(csrf -> csrf.disable()); // API de token sem estado; sem cookie de sessão
        return http.build();
    }
}
```

Se senhas forem armazenadas, use hash com argon2 ou bcrypt (nunca um digest simples), limite a taxa de login e exija MFA para administradores.

## Autorização

Autorize toda solicitação, negue por padrão e imponha privilégio mínimo. Use segurança de método para verificar papéis e valide explicitamente a propriedade do recurso.

```java
@PreAuthorize("hasRole('AUDITOR')")
public AuditReport generate(UUID resourceId, Authentication principal) {
    Resource resource = resourceService.getOwned(resourceId, principal.getName());
    // a propriedade é verificada no serviço; somente o papel não basta
    return AuditReport.of(resource);
}
```

## Validação de entrada e injeção

Valide em todo limite com `@Valid` (consulte [`backend.instructions.md`](backend.instructions.md)). Crie consultas somente com parâmetros associados JPA/JPQL, escape HTML na saída e valide uploads por tipo e tamanho.

> [!WARNING]
> Nunca concatene entrada da pessoa usuária em uma consulta, comando de shell ou marcação. SQL construído por strings é o vetor clássico de injeção; a associação de parâmetros é obrigatória.

## CORS

Configure explicitamente as origens permitidas. O curinga `*` é proibido em produção.

```java
@Bean
CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://app.example.gov.br")); // nunca use "*" em produção
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}
```

## Segredos e configuração segura

Nenhum segredo é fixado no código, versionado ou registrado. Leia segredos do ambiente ou do Key Vault; use Managed Identity na autenticação serviço a serviço do Azure. No frontend, somente valores não secretos podem usar o prefixo `NEXT_PUBLIC_`; todo valor prefixado é enviado ao navegador.

## Dados sensíveis (CPF, valores)

> [!IMPORTANT]
> Mascare campos regulamentados (CPF, valores de benefícios) em logs, respostas de erro e URLs. Nunca os coloque em query strings nem em armazenamento sem criptografia e sempre transmita por TLS.

```java
// mantém os 3 primeiros e os 2 últimos dígitos de um CPF com 11 dígitos
String masked = cpf.replaceAll("(\\d{3})\\d{6}(\\d{2})", "$1******$2");
```

## Limite de autenticação do frontend (`middleware.ts`)

Proteja rotas no middleware; nunca confie no cliente para impor acesso. Mantenha tokens e segredos no servidor.

```ts
import { NextResponse, type NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const session = request.cookies.get('session');
  if (!session) return NextResponse.redirect(new URL('/login', request.url));
  return NextResponse.next();
}

export const config = { matcher: ['/dashboard/:path*'] };
```

## Limites de automação e agentes

Um agente de IA ou automação nunca concede novas permissões a si mesmo nem acessa um banco de dados de produção sem aprovação humana explícita. Mudanças em autenticação, papéis ou tratamento de segredos exigem revisão por pares antes do merge.

## Convenções

| Regra | Justificativa |
|---|---|
| OAuth2/JWT via Spring Security | Sem código personalizado de autenticação sujeito a erros |
| Autorize toda solicitação e negue por padrão | Privilégio mínimo em cada limite |
| Somente parâmetros associados JPA/JPQL | Elimina injeção de SQL |
| Origens CORS explícitas, sem `*` em produção | Bloqueia abuso entre origens |
| Segredos do ambiente/Key Vault, Managed Identity | Sem credenciais no código ou nos logs |
| Mascare CPF e valores em todos os locais | Protege dados regulamentados |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Gere hash de senhas com argon2/bcrypt | Armazene ou registre texto simples ou digest simples |
| Verifique o papel **e** a propriedade do recurso | Trate um papel como autorização suficiente |
| Mantenha segredos no servidor | Prefixe um segredo com `NEXT_PUBLIC_` |
| Mascare campos sensíveis antes do log | Coloque CPF/valores em logs ou query strings |

## Lista de verificação antes de abrir uma PR

- [ ] Os endpoints autenticam via Spring Security; não há análise personalizada de tokens
- [ ] Toda solicitação é autorizada, com negação por padrão e verificação de propriedade quando pertinente
- [ ] Todas as consultas usam parâmetros associados; uploads e entradas são validados
- [ ] O CORS lista origens explícitas; não há `*` na configuração de produção
- [ ] Nenhum segredo está fixado no código, versionado ou registrado; a autenticação Azure usa Managed Identity
- [ ] CPF, valores e tokens estão mascarados em logs, erros e URLs
