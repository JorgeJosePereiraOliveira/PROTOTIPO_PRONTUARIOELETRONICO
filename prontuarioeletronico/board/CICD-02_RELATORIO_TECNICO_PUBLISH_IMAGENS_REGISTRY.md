# CICD-02 - Relatorio Tecnico (Publish de imagens no registry)

- **Data de fechamento tecnico:** 2026-03-13
- **Issue alvo:** #18 CICD-02 Publish de imagens e promocao de artefatos
- **Objetivo:** automatizar publicacao versionada de imagens de microsservicos em registry, com rastreabilidade por digest e reaproveitamento de artefatos SBOM da pipeline.

---

## 1) Escopo executado

1. Inclusao de job de publicacao de imagens no workflow de CI.
2. Publicacao automatica no GHCR para os 7 servicos.
3. Versionamento por commit (`sha`) e tag operacional (`main`).
4. Reuso dos SBOMs produzidos no `security-baseline`.
5. Emissao de metadados de rastreabilidade (service, tags, digest, referencia de SBOM e run).

---

## 2) Mudancas tecnicas realizadas

### 2.1 Workflow atualizado

Arquivo alterado:
- `.github/workflows/python-ci.yml`

Job adicionado:
- `cicd-publish-images`

Caracteristicas do job:
- executa somente em `push` para `main`;
- depende dos gates de qualidade e seguranca:
  - `core-tests`
  - `auth-service-tests`
  - `patient-service-tests`
  - `emr-service-tests`
  - `scheduling-service-tests`
  - `audit-service-tests`
  - `professional-service-tests`
  - `gateway-integration-tests`
  - `api-compatibility-check`
  - `security-baseline`
- usa matrix para os 7 servicos (`auth`, `patient`, `emr`, `scheduling`, `audit`, `professional`, `gateway`);
- autentica em `ghcr.io` com `GITHUB_TOKEN` (`packages: write`);
- publica imagens com tags:
  - `ghcr.io/<owner>/prontuario-<service>:<sha>`
  - `ghcr.io/<owner>/prontuario-<service>:main`

### 2.2 Reuso de SBOM e rastreabilidade de artefatos

- O job faz download do artifact `sbom-cyclonedx-docker03` gerado no `security-baseline`.
- Para cada servico, e gerado artifact de trilha em JSON (`artifact-trace-<service>`), contendo:
  - nome do servico;
  - repositorio da imagem no GHCR;
  - tags publicadas;
  - digest da imagem publicada;
  - referencia do arquivo SBOM;
  - URL do workflow run.

Resultado: artefatos versionados e rastreaveis por commit, digest e evidencias de seguranca.

---

## 3) Criterios de aceite (resultado)

- [x] Artefatos publicados com versionamento por commit/tag.
- [x] Rastreabilidade por digest e metadados por servico.
- [x] Publicacao condicionada a gates de qualidade e seguranca.
- [x] Reaproveitamento dos artefatos SBOM no fluxo de publicacao.

---

## 4) Conclusao

A CICD-02 estabelece a etapa de publicacao de artefatos em registry de forma controlada e auditavel, conectando qualidade (testes e compatibilidade), seguranca (scan/SBOM) e distribuicao de imagens (GHCR) em uma unica esteira de entrega. A abordagem reduz risco de promocao de artefatos sem evidencia tecnica e prepara base para a etapa seguinte de promocao progressiva e deploy continuo.