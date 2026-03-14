# K8S-03 - Relatorio Tecnico (ConfigMap/Secret/NetworkPolicy/limits)

- **Data de fechamento tecnico:** 2026-03-14
- **Issue alvo:** #21 K8S-03 ConfigMap/Secret/NetworkPolicy/limits
- **Objetivo:** endurecer a operacao em cluster com politicas de configuracao, isolamento de rede e guardrails de recursos.

---

## 1) Escopo executado

1. Consolidacao de configuracao por ambiente via `ConfigMap` e `Secret`.
2. Inclusao de politicas de hardening em Kubernetes:
   - `LimitRange`
   - `ResourceQuota`
   - `NetworkPolicy` (default deny e regras de liberacao minima)
3. Validacao automatizada de politicas ativas no deploy de homolog.
4. Publicacao de evidencias de aplicacao no artifact de deploy Kubernetes.

---

## 2) Mudancas tecnicas realizadas

### 2.1 Manifestos de hardening

Arquivo alterado:
- `prontuarioeletronico/scripts/render_k8s_manifests_from_trace.sh`

Adicao do arquivo renderizado:
- `40-hardening.yaml` contendo:
  - `LimitRange` (`workload-defaults`)
  - `ResourceQuota` (`namespace-quota`)
  - `NetworkPolicy`:
    - `default-deny-egress`
    - `allow-egress-intra-namespace`
    - `allow-egress-dns`

### 2.2 Validacao no fluxo de deploy homolog

Arquivo alterado:
- `prontuarioeletronico/scripts/deploy_k8s_homolog.sh`

Adicoes:
- aplicacao de `40-hardening.yaml`;
- verificacoes de presenca/atividade de `LimitRange`, `ResourceQuota` e `NetworkPolicy`;
- inclusao de inventario dessas politicas no relatorio de deploy (`rollout-report/k8s-homolog-deploy-report.md`).

---

## 3) Criterios de aceite (resultado)

- [x] Politicas de configuracao e hardening aplicadas no namespace de homolog.
- [x] NetworkPolicies ativas e validadas no pipeline.
- [x] Guardrails de recursos (limits/quota) ativos e auditaveis.

---

## 4) Conclusao

A K8S-03 conclui a camada de hardening basico da operacao em cluster, adicionando isolamento de egress, governanca de recursos e verificacao automatizada de politicas no pipeline. O resultado fortalece seguranca e previsibilidade operacional do ambiente de homolog, mantendo rastreabilidade completa das evidencias de aplicacao.