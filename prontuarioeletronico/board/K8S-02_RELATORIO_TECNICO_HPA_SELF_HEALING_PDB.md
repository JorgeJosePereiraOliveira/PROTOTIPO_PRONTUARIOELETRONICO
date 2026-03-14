# K8S-02 - Relatorio Tecnico (HPA + self-healing + PDB)

- **Data de fechamento tecnico:** 2026-03-14
- **Issue alvo:** #20 K8S-02 HPA + self-healing + PDB
- **Objetivo:** adicionar escalabilidade automatica e validacao de recuperacao autonoma de falhas no ambiente de homolog Kubernetes.

---

## 1) Escopo executado

1. Implementacao de HPA para servicos criticos:
   - `auth-service`
   - `patient-service`
   - `gateway-service`
2. Implementacao de PDB para os mesmos servicos criticos.
3. Ajuste de requests/limits de recursos para permitir autoscaling por CPU.
4. Automacao de teste de self-healing por falha induzida de pod em homolog.
5. Integracao da validacao ao pipeline K8S em cluster `kind`/externo.

---

## 2) Mudancas tecnicas realizadas

### 2.1 Renderizacao de manifests de resiliencia

Arquivo alterado:
- `prontuarioeletronico/scripts/render_k8s_manifests_from_trace.sh`

Adicoes:
- `30-resilience.yaml` com:
  - HPAs (`autoscaling/v2`) para `auth-service`, `patient-service`, `gateway-service`;
  - PDBs (`policy/v1`) para os tres servicos criticos;
- replicas base ajustadas para servicos criticos (`replicas: 2`);
- recursos de container definidos (`requests` e `limits`) para viabilizar HPA por CPU.

### 2.2 Validacao de resiliencia no deploy de homolog

Arquivo alterado:
- `prontuarioeletronico/scripts/deploy_k8s_homolog.sh`

Adicoes:
- aplicacao de `30-resilience.yaml`;
- verificacao de presenca de HPA/PDB apos deploy;
- teste de self-healing automatizado:
  - delecao de pod de `auth-service` e `gateway-service`;
  - espera por `rollout status`;
  - validacao de substituicao por novo pod.

### 2.3 Suporte de HPA no cluster kind do CI

Arquivo alterado:
- `.github/workflows/python-ci.yml`

Adicao no job `k8s-deploy-homolog`:
- instalacao de `metrics-server` no caminho `kind`;
- patch de `--kubelet-insecure-tls`;
- espera por readiness do deployment `metrics-server`.

---

## 3) Criterios de aceite (resultado)

- [x] HPA ativo para servicos criticos em homolog.
- [x] PDB aplicado para servicos criticos.
- [x] Teste de falha com recuperacao automatica executado no pipeline.

---

## 4) Conclusao

A K8S-02 elevou a maturidade operacional da camada Kubernetes ao introduzir autoscaling orientado a recurso, protecao de disponibilidade em manutencao/eviccao e evidencias automatizadas de self-healing. A validacao integrada ao pipeline reforca confiabilidade e reduz risco de regressao de resiliencia nas proximas iteracoes.