# CICD-03 - Relatorio Tecnico (CD progressivo com rollback automatico)

- **Data de fechamento tecnico:** 2026-03-14
- **Issue alvo:** #22 CICD-03 CD progressivo com rollback automatico
- **Objetivo:** habilitar promocao progressiva de artefatos em registry com mecanismo automatico de rollback em caso de violacao de SLO.

---

## 1) Escopo executado

1. Inclusao de etapa de CD progressivo no workflow principal.
2. Reuso dos `artifact-trace-*` da CICD-02 para promover imagens por digest.
3. Estrategia de promocao por estagios de release:
   - `dev`
   - `homolog`
   - `prod-canary`
   - `prod`
4. Implementacao de rollback automatico com restauracao para `prod-rollback` quando houver violacao de SLO.
5. Publicacao de evidencia auditavel da promocao em artifact de run.

---

## 2) Mudancas tecnicas realizadas

### 2.1 Workflow CI/CD atualizado

Arquivo alterado:
- `.github/workflows/python-ci.yml`

Adicoes principais:
1. `workflow_dispatch` com input `simulate_slo_breach` para validacao controlada do caminho de rollback.
2. Job novo `cicd-progressive-cd` dependente de `cicd-publish-images`.
3. Download de `artifact-trace-*` para consolidar metadata por servico.
4. Execucao do script de promocao progressiva e rollback automatico.
5. Upload do artifact `progressive-rollout-report` com resumo auditavel da decisao por servico.

### 2.2 Script de rollout progressivo

Arquivo criado:
- `prontuarioeletronico/scripts/progressive_cd_with_rollback.sh`

Funcionalidades:
- leitura dos traces gerados na CICD-02;
- promocao por digest com tags de estagio (`dev`, `homolog`, `prod-canary`, `prod`);
- snapshot de `prod` em `prod-rollback` quando existente;
- rollback automatico para `prod-rollback` em violacao de SLO;
- geracao de relatorio markdown consolidado em `rollout-report/progressive-rollout-summary.md`.

---

## 3) Criterios de aceite (resultado)

- [x] Estrategia progressiva disponibilizada (canary por tag `prod-canary`).
- [x] Rollback automatico implementado e acionavel por gate de SLO.
- [x] Evidencia de deployment/promocao auditavel via artifact de run.

---

## 4) Conclusao

A CICD-03 foi implementada como fatia executavel orientada a risco operacional: o pipeline passa a promover artefatos por estagios com trilha de auditoria e resposta automatica a violacao de SLO por rollback, aproveitando integralmente os digests e metadados de rastreabilidade estabelecidos na CICD-02.