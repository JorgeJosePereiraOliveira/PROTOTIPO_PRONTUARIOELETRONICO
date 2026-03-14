# K8S-01 - Deploy base por servico

Este diretorio consolida os artefatos de deploy Kubernetes da K8S-01.

## Objetivo

Conectar a promocao progressiva (CICD-03) ao deploy real em cluster de homolog, usando os digests publicados no registry e rastreados por `artifact-trace-*`.

## Fluxo de CI/CD

1. `cicd-publish-images` publica imagens no GHCR e gera `artifact-trace-*`.
2. `cicd-progressive-cd` promove por estagios (`dev`, `homolog`, `prod-canary`, `prod`).
3. `k8s-deploy-homolog` consome os traces e aplica manifests no cluster.

## Scripts

- `prontuarioeletronico/scripts/render_k8s_manifests_from_trace.sh`
  - Renderiza namespace, config/secret, deployments/services e ingress com imagem `repository@digest`.
- `prontuarioeletronico/scripts/deploy_k8s_homolog.sh`
  - Aplica manifests no cluster e valida rollout de todos os deployments.

## Segredos necessarios no GitHub

- `KUBE_CONFIG_DATA`: kubeconfig do cluster em Base64.
- `AUTH_JWT_SECRET_HOMOLOG`: segredo JWT para `auth-service` em homolog.

Sem esses segredos, o job de deploy em cluster e ignorado para nao quebrar a esteira de CI.
