#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-prontuarioeletronico}"
SERVICES=(
  auth-service
  patient-service
  emr-service
  scheduling-service
  audit-service
  professional-service
  gateway-service
)

TRIVY_IMAGE="${TRIVY_IMAGE:-aquasec/trivy:0.63.0}"
SYFT_IMAGE="${SYFT_IMAGE:-anchore/syft:v1.24.0}"
SBOM_DIR="${ROOT_DIR}/board/sbom"

mkdir -p "${SBOM_DIR}"

for service in "${SERVICES[@]}"; do
  image="tcc/${service}:docker03-ci"
  context_path="${ROOT_DIR}/services/${service}"

  echo "[DOCKER-03] Building ${image} from ${context_path}"
  docker build -t "${image}" "${context_path}"

  echo "[DOCKER-03] Scanning critical CVEs in ${image}"
  docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    "${TRIVY_IMAGE}" image \
    --scanners vuln \
    --severity CRITICAL \
    --ignore-unfixed \
    --skip-version-check \
    --exit-code 1 \
    --no-progress \
    "${image}"

  sbom_file="${SBOM_DIR}/${service}.cdx.json"
  echo "[DOCKER-03] Generating SBOM for ${image} -> ${sbom_file}"
  docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "${PWD}:/workdir" \
    "${SYFT_IMAGE}" "${image}" \
    -o "cyclonedx-json=/workdir/${sbom_file}"
done

echo "[DOCKER-03] Completed. SBOM artifacts available in ${SBOM_DIR}"
