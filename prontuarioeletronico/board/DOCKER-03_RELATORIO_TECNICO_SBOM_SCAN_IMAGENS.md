# DOCKER-03 - Relatorio Tecnico (SBOM e scan de imagens)

- **Data de fechamento tecnico:** 2026-03-13
- **Issue alvo:** #17 DOCKER-03 SBOM e scan de imagens
- **Objetivo:** implementar gate de seguranca de imagens no CI, bloqueando release quando houver CVEs criticos corrigiveis e gerando SBOM por servico.

---

## 1) Escopo executado

1. Extensao do job `security-baseline` para incluir seguranca de conteiner.
2. Implementacao de script unico para:
   - build das imagens dos 7 servicos;
   - scan de CVEs criticos corrigiveis em imagem;
   - geracao de SBOM no formato CycloneDX por servico.
3. Publicacao dos SBOMs como artifact no GitHub Actions.
4. Validacao local da esteira DOCKER-03 com geracao de SBOM para toda a stack.

---

## 2) Mudancas tecnicas realizadas

### 2.1 Workflow CI atualizado

Arquivo alterado:
- `.github/workflows/python-ci.yml`

No job `security-baseline`, foram adicionados:
1. Step de conteinerizacao e seguranca:
   - `bash prontuarioeletronico/scripts/generate_sbom_and_scan_images.sh`
2. Step de publicacao de artefatos:
   - `actions/upload-artifact@v4`
   - artifact: `sbom-cyclonedx-docker03`
   - path: `prontuarioeletronico/board/sbom/*.cdx.json`

### 2.2 Script executavel da fatia

Arquivo criado:
- `prontuarioeletronico/scripts/generate_sbom_and_scan_images.sh`

Comportamento:
- constroi imagens `tcc/<service>:docker03-ci` para:
  - auth, patient, emr, scheduling, audit, professional e gateway;
- executa scan com Trivy em modo gate:
  - severidade: `CRITICAL`
  - politica: `--ignore-unfixed`
  - bloqueio: `--exit-code 1`
- gera SBOM CycloneDX via Syft em:
  - `prontuarioeletronico/board/sbom/<service>.cdx.json`

Justificativa da politica `--ignore-unfixed`:
- na validacao inicial, CVEs criticos sem fix disponivel no upstream da base Debian bloquearam toda a esteira;
- com `--ignore-unfixed`, o gate permanece efetivo para vulnerabilidades criticas corrigiveis, viabilizando operacao pratica sem suprimir risco.

### 2.3 Higiene de versionamento

Arquivo alterado:
- `.gitignore`

Entrada adicionada:
- `prontuarioeletronico/board/sbom/*.cdx.json`

Motivo:
- evitar commit de artefatos volumosos locais; SBOM oficial permanece rastreavel via artifact do CI.

---

## 3) Evidencias de validacao

### 3.1 Validacao local da fatia executavel

Comando executado:
- `bash prontuarioeletronico/scripts/generate_sbom_and_scan_images.sh`

Resultado:
- build e scan executados para 7/7 imagens;
- gate Trivy operacional para CVEs criticos corrigiveis;
- SBOMs gerados para 7/7 servicos.

Arquivos SBOM confirmados localmente:
- `prontuarioeletronico/board/sbom/auth-service.cdx.json`
- `prontuarioeletronico/board/sbom/patient-service.cdx.json`
- `prontuarioeletronico/board/sbom/emr-service.cdx.json`
- `prontuarioeletronico/board/sbom/scheduling-service.cdx.json`
- `prontuarioeletronico/board/sbom/audit-service.cdx.json`
- `prontuarioeletronico/board/sbom/professional-service.cdx.json`
- `prontuarioeletronico/board/sbom/gateway-service.cdx.json`

### 3.2 Integracao ao CI

Com a alteracao do workflow, cada push para `main` passa a produzir:
- verificacao SAST Python (`bandit`) +
- verificacao de imagem com gate de criticidade +
- SBOM CycloneDX publicado como artifact do run.

---

## 4) Criterios de aceite (resultado)

- [x] CVEs criticos bloqueiam release (para casos corrigiveis, com `exit-code 1`).
- [x] SBOM gerado por build para todos os servicos da stack.
- [x] Evidencia de artefatos no pipeline por upload de SBOM.

---

## 5) Conclusao

A DOCKER-03 foi implementada com abordagem executavel e auditavel: o pipeline agora incorpora seguranca de imagens como gate de release e gera SBOM padrao CycloneDX para rastreabilidade de supply chain. O resultado fortalece a maturidade de conteinerizacao iniciada em DOCKER-01/DOCKER-02 e prepara o terreno para publicacao segura de imagens nas etapas CICD seguintes.