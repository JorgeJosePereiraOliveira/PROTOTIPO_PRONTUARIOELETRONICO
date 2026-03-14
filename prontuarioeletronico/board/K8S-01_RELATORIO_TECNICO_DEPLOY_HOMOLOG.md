# K8S-01 - Relatorio Tecnico (Deployments/Services/Ingress por servico)

- **Data de inicio tecnico:** 2026-03-14
- **Issue alvo:** #19 K8S-01 Deployments/Services/Ingress por servico
- **Objetivo da fatia inicial:** conectar a promocao progressiva (CICD-03) ao deploy real em cluster de homolog a partir de digests rastreados.

---

## 1) Escopo implementado nesta fatia

1. Renderizacao automatica de manifests Kubernetes por digest de imagem (trace da CICD-02/CICD-03).
2. Estrutura base de deploy por servico com:
   - `Deployment`
   - `Service`
   - `Ingress` (gateway)
3. Probes de saude em todos os pods (`readiness` e `liveness` em `/health`).
4. Configuracao por ambiente via `ConfigMap` e `Secret`.
5. Job de deploy homolog no workflow CI/CD com evidencias de rollout.

---

## 2) Artefatos tecnicos criados

- Script de render dos manifests:
  - `prontuarioeletronico/scripts/render_k8s_manifests_from_trace.sh`
- Script de deploy em homolog:
  - `prontuarioeletronico/scripts/deploy_k8s_homolog.sh`
- Guia de uso K8S-01:
  - `prontuarioeletronico/k8s/README_K8S_01.md`
- Workflow atualizado com job `k8s-deploy-homolog`:
  - `.github/workflows/python-ci.yml`

---

## 3) Comportamento do deploy homolog

O job `k8s-deploy-homolog`:
1. baixa os `artifact-trace-*` gerados na esteira;
2. renderiza manifests para o namespace `prontuario-homolog` com imagem imutavel (`repository@digest`);
3. aplica recursos no cluster via `kubectl`;
4. valida rollout dos 7 deployments;
5. publica artefatos de evidência (`k8s-homolog-deploy-artifacts`).

Precondicoes de execucao em cluster:
- `KUBE_CONFIG_DATA` (base64 do kubeconfig)
- `AUTH_JWT_SECRET_HOMOLOG`

---

## 4) Estado atual da fatia

- [x] Conexao CICD-03 -> K8S-01 implementada tecnicamente no pipeline.
- [x] Manifests base por servico com probes e configuracao por ambiente.
- [ ] Validacao de deploy real em cluster homolog pendente de disponibilidade/configuracao de segredos do cluster no repositório.

---

## 5) Proximo passo operacional

1. Configurar segredos de cluster (`KUBE_CONFIG_DATA`, `AUTH_JWT_SECRET_HOMOLOG`).
2. Executar workflow e confirmar rollout em homolog.
3. Coletar URL/evidencias finais para encerramento formal da issue #19.
