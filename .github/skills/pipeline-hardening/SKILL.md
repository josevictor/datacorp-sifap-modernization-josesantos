---
name: "pipeline-hardening"
description: "Use ao fortalecer um fluxo de CI/CD, migrar para OIDC, assinar artefatos ou atender aos requisitos SLSA. Os gatilhos incluem \"SLSA\", \"cadeia de suprimentos\", \"OIDC\", \"sigstore\", \"cosign\", \"segurança do fluxo de CI/CD\" e \"fortalecimento de GHA\"."
---
# Fortalecimento do fluxo de CI/CD

## Quando invocar

- "Fortaleça nosso fluxo de CI/CD do GitHub Actions / Azure DevOps / GitLab."
- "Migre de segredos de longa duração para OIDC."
- "Alcance o SLSA Nível 2/3."
- "Assine nossas imagens de contêiner."

## Modelo de ameaças (lista resumida)

1. **Segredos roubados** de registros do fluxo de CI/CD ou de um executor comprometido.
2. **Dependência maliciosa** publicada na origem ou por registro de nomes semelhantes (typosquatting).
3. **GitHub Action de terceiros ou etapa compartilhada comprometida**.
4. **Artefato adulterado** entre o build e a implantação.
5. **Escalação de privilégios** causada por permissões excessivamente amplas no fluxo de CI/CD.

## Controles (ordenados por retorno sobre investimento, ROI)

### Nível 1: faça primeiro

- [ ] **OIDC para a nuvem**: não armazene credenciais de nuvem de longa duração como segredos. Use identidade federada com tokens de curta duração.
- [ ] **Fixe as ações de terceiros por SHA**, não por tag (`actions/checkout@<sha>` com um comentário que mostre a versão).
- [ ] Inclua um **bloco `permissions:`** em cada fluxo de trabalho, com `contents: read` como padrão e elevação somente quando necessária.
- [ ] **Proteção de ramificação**: revisões e verificações de status obrigatórias, sem envio forçado (force push) e com registros de alteração assinados (commits) na `main`.
- [ ] Habilite **verificação de segredos e proteção contra envio** em toda a organização.
- [ ] Use **Dependabot / Renovate** para dependências e ações.

### Nível 2: integridade da cadeia de suprimentos

- [ ] **Lista de materiais de software (SBOM)** gerada para cada compilação (Syft / CycloneDX).
- [ ] **Assinatura de artefatos** com Cosign (preferencialmente sem chave via OIDC).
- [ ] **Proveniência** (atestação SLSA v1.0) publicada com o artefato.
- [ ] **Verificação de assinaturas durante a implantação**: a tarefa de implantação rejeita artefatos não assinados.
- [ ] **Verificação de vulnerabilidades** (Trivy / Grype) na imagem; falha em achados Critical/High, salvo exceções justificadas.

### Nível 3: maduro

- [ ] **Compilações herméticas e reproduzíveis** quando viável.
- [ ] **Revisão por duas pessoas** nos fluxos de lançamento.
- [ ] **Fortalecimento de executores**: efêmeros, com saída de rede restrita e sem estado mutável compartilhado.

## Antipadrões

- Armazenar `AWS_ACCESS_KEY_ID` / `AZURE_CLIENT_SECRET` como segredos do repositório quando OIDC está disponível.
- `permissions: write-all`.
- Tags flutuantes `@main` ou `@v3` em ações de terceiros.
- Implantar um artefato criado em outro fluxo de CI/CD sem verificar sua assinatura.
- Exibir segredos em registros por meio de expansão do interpretador de comandos sem aspas.

## Modelo de saída

```markdown
## Relatório de fortalecimento do fluxo de CI/CD - <fluxo de trabalho ou repositório>

| Controle | Status | Evidência / lacuna |
|---|---|---|
| OIDC para autenticação na nuvem | concluído / ausente | <endereço ou observação> |
| Ações fixadas por SHA | concluído / ausente | <quantidade de tags flutuantes> |
| Permissões de privilégio mínimo | concluído / ausente | <fluxos de trabalho sem o bloco> |
| SBOM + assinatura de artefatos | concluído / ausente | <ferramenta> |
| Proveniência (SLSA) | Nível 0/1/2/3 | <endereço da atestação> |

**Nível SLSA desejado**: <N>
**Lacunas impeditivas**: <quantidade>
```

## Critérios de qualidade

- [ ] Não restam segredos de nuvem de longa duração; a autenticação na nuvem usa federação OIDC.
- [ ] Cada ação de terceiros está fixada pelo SHA do registro de alteração, não por uma tag flutuante.
- [ ] Cada fluxo de trabalho declara um bloco `permissions:` de privilégio mínimo (`contents: read` por padrão).
- [ ] Os artefatos de lançamento estão assinados, e as assinaturas são verificadas durante a implantação.
- [ ] A verificação de segredos, a proteção contra envio e as atualizações de dependências estão habilitadas.

## Referências

- [SLSA v1.0](https://slsa.dev/spec/v1.0/)
- [GitHub - Fortalecimento de segurança para GHA](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Sigstore / Cosign](https://docs.sigstore.dev/)
- [OpenSSF Scorecard](https://scorecard.dev/)
