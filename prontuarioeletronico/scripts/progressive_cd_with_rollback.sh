#!/usr/bin/env bash
set -euo pipefail

: "${TRACE_DIR:?TRACE_DIR is required}"
SIMULATE_SLO_BREACH="${SIMULATE_SLO_BREACH:-false}"
GIT_REF_SHA="${GITHUB_SHA:-local}"

mkdir -p rollout-report
report_file="rollout-report/progressive-rollout-summary.md"

shopt -s nullglob
trace_files=("${TRACE_DIR}"/*.json)
if [ "${#trace_files[@]}" -eq 0 ]; then
  echo "No artifact trace files found in ${TRACE_DIR}" >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python interpreter not found (python3/python)." >&2
  exit 1
fi

read_trace_field() {
  local trace_file="$1"
  local field_name="$2"
  "$PYTHON_BIN" - "$trace_file" "$field_name" <<'PY'
import json
import sys

file_path = sys.argv[1]
field = sys.argv[2]
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
value = data.get(field, "")
if value is None:
    value = ""
print(value)
PY
}

overall_breach=false

{
  echo "# CICD-03 Progressive CD Summary"
  echo
  echo "- Simulate SLO breach: ${SIMULATE_SLO_BREACH}"
  echo "- Trace directory: ${TRACE_DIR}"
  echo
  echo "| Service | Digest | Action | Result |"
  echo "|---|---|---|---|"

  for trace_file in "${trace_files[@]}"; do
    service="$(read_trace_field "${trace_file}" service)"
    repository="$(read_trace_field "${trace_file}" repository)"
    digest="$(read_trace_field "${trace_file}" digest)"

    if [ -z "${service}" ] || [ -z "${repository}" ] || [ -z "${digest}" ] || [ "${digest}" = "null" ]; then
      echo "Invalid trace metadata in ${trace_file}" >&2
      exit 1
    fi

    echo "Promoting ${service} from ${repository}@${digest}"

    docker buildx imagetools create \
      -t "${repository}:dev" \
      -t "${repository}:dev-${GIT_REF_SHA}" \
      "${repository}@${digest}" >/dev/null

    docker buildx imagetools create \
      -t "${repository}:homolog" \
      -t "${repository}:homolog-${GIT_REF_SHA}" \
      "${repository}@${digest}" >/dev/null

    previous_prod_available=false
    if docker buildx imagetools inspect "${repository}:prod" >/dev/null 2>&1; then
      previous_prod_available=true
      docker buildx imagetools create -t "${repository}:prod-rollback" "${repository}:prod" >/dev/null
    fi

    docker buildx imagetools create \
      -t "${repository}:prod-canary" \
      -t "${repository}:prod-canary-${GIT_REF_SHA}" \
      "${repository}@${digest}" >/dev/null

    if [ "${SIMULATE_SLO_BREACH}" = "true" ]; then
      overall_breach=true
      if [ "${previous_prod_available}" = "true" ]; then
        docker buildx imagetools create -t "${repository}:prod" "${repository}:prod-rollback" >/dev/null
        echo "| ${service} | ${digest} | rollback (SLO breach) | restored previous prod |"
      else
        echo "| ${service} | ${digest} | rollback (SLO breach) | no previous prod, kept canary only |"
      fi
      continue
    fi

    docker buildx imagetools create \
      -t "${repository}:prod" \
      -t "${repository}:prod-${GIT_REF_SHA}" \
      "${repository}@${digest}" >/dev/null

    echo "| ${service} | ${digest} | progressive promotion | dev -> homolog -> prod-canary -> prod |"
  done
} > "${report_file}"

if [ "${overall_breach}" = "true" ]; then
  echo "SLO breach simulated. Automatic rollback path executed." >&2
  exit 1
fi

echo "Progressive rollout finished successfully."
