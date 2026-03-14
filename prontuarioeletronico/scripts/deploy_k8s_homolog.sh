#!/usr/bin/env bash
set -euo pipefail

: "${KUBE_CONFIG:?KUBE_CONFIG is required}"
: "${MANIFEST_DIR:?MANIFEST_DIR is required}"
NAMESPACE="${NAMESPACE:-prontuario-homolog}"

export KUBECONFIG="${KUBE_CONFIG}"

kubectl apply -f "${MANIFEST_DIR}/00-namespace.yaml"
kubectl apply -f "${MANIFEST_DIR}/10-services.yaml"
kubectl apply -f "${MANIFEST_DIR}/20-ingress.yaml"
if [ -f "${MANIFEST_DIR}/30-resilience.yaml" ]; then
  kubectl apply -f "${MANIFEST_DIR}/30-resilience.yaml"
fi
if [ -f "${MANIFEST_DIR}/40-hardening.yaml" ]; then
  kubectl apply -f "${MANIFEST_DIR}/40-hardening.yaml"
fi

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

hpa_targets=(
  auth-service
  patient-service
  gateway-service
)

{
  echo
  echo "## HPA and PDB"
} >> "${report_file}"

for target in "${hpa_targets[@]}"; do
  kubectl -n "${NAMESPACE}" get hpa "${target}-hpa" >/dev/null
  kubectl -n "${NAMESPACE}" get pdb "${target}-pdb" >/dev/null
  echo "- ${target}: HPA and PDB present" >> "${report_file}"
done

{
  echo
  echo "## Hardening policies"
} >> "${report_file}"

kubectl -n "${NAMESPACE}" get limitrange workload-defaults >/dev/null
kubectl -n "${NAMESPACE}" get resourcequota namespace-quota >/dev/null
kubectl -n "${NAMESPACE}" get networkpolicy default-deny-egress >/dev/null
kubectl -n "${NAMESPACE}" get networkpolicy allow-egress-intra-namespace >/dev/null
kubectl -n "${NAMESPACE}" get networkpolicy allow-egress-dns >/dev/null

echo "- limitrange/workload-defaults: active" >> "${report_file}"
echo "- resourcequota/namespace-quota: active" >> "${report_file}"
echo "- networkpolicy/default-deny-egress: active" >> "${report_file}"
echo "- networkpolicy/allow-egress-intra-namespace: active" >> "${report_file}"
echo "- networkpolicy/allow-egress-dns: active" >> "${report_file}"

self_heal_targets=(
  auth-service
  gateway-service
)

{
  echo
  echo "## Self-healing validation"
} >> "${report_file}"

for target in "${self_heal_targets[@]}"; do
  old_pod="$(kubectl -n "${NAMESPACE}" get pod -l app="${target}" -o jsonpath='{.items[0].metadata.name}')"
  kubectl -n "${NAMESPACE}" delete pod "${old_pod}" --wait=false >/dev/null
  kubectl -n "${NAMESPACE}" rollout status "deployment/${target}" --timeout=180s >/dev/null

  recovered="false"
  for _ in $(seq 1 30); do
    new_pod="$(kubectl -n "${NAMESPACE}" get pod -l app="${target}" -o jsonpath='{.items[0].metadata.name}')"
    if [ "${new_pod}" != "${old_pod}" ]; then
      recovered="true"
      break
    fi
    sleep 2
  done

  if [ "${recovered}" != "true" ]; then
    echo "Self-healing failed for ${target}: replacement pod was not observed" >&2
    exit 1
  fi

  echo "- ${target}: pod failure recovered automatically" >> "${report_file}"
done

{
  echo
  echo "## Resources"
  kubectl -n "${NAMESPACE}" get deploy -o wide
  echo
  kubectl -n "${NAMESPACE}" get svc -o wide
  echo
  kubectl -n "${NAMESPACE}" get ingress -o wide
  echo
  kubectl -n "${NAMESPACE}" get hpa -o wide
  echo
  kubectl -n "${NAMESPACE}" get pdb -o wide
  echo
  kubectl -n "${NAMESPACE}" get limitrange -o wide
  echo
  kubectl -n "${NAMESPACE}" get resourcequota -o wide
  echo
  kubectl -n "${NAMESPACE}" get networkpolicy -o wide
} >> "${report_file}"

echo "Kubernetes homolog deployment completed successfully"
