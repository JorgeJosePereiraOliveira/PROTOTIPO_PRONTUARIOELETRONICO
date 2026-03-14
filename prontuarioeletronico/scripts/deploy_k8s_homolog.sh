#!/usr/bin/env bash
set -euo pipefail

: "${KUBE_CONFIG:?KUBE_CONFIG is required}"
: "${MANIFEST_DIR:?MANIFEST_DIR is required}"
NAMESPACE="${NAMESPACE:-prontuario-homolog}"

export KUBECONFIG="${KUBE_CONFIG}"

kubectl apply -f "${MANIFEST_DIR}/00-namespace.yaml"
kubectl apply -f "${MANIFEST_DIR}/10-services.yaml"
kubectl apply -f "${MANIFEST_DIR}/20-ingress.yaml"

services=(
  auth-service
  patient-service
  emr-service
  scheduling-service
  audit-service
  professional-service
  gateway-service
)

mkdir -p rollout-report
report_file="rollout-report/k8s-homolog-deploy-report.md"

{
  echo "# K8S-01 Homolog Deployment Report"
  echo
  echo "- Namespace: ${NAMESPACE}"
  echo
  echo "## Rollout status"
} > "${report_file}"

for service in "${services[@]}"; do
  kubectl -n "${NAMESPACE}" rollout status "deployment/${service}" --timeout=180s
  echo "- ${service}: rollout successful" >> "${report_file}"
done

{
  echo
  echo "## Resources"
  kubectl -n "${NAMESPACE}" get deploy -o wide
  echo
  kubectl -n "${NAMESPACE}" get svc -o wide
  echo
  kubectl -n "${NAMESPACE}" get ingress -o wide
} >> "${report_file}"

echo "Kubernetes homolog deployment completed successfully"
