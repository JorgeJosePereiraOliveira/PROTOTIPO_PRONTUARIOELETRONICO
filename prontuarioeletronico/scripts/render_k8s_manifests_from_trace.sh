#!/usr/bin/env bash
set -euo pipefail

: "${TRACE_DIR:?TRACE_DIR is required}"
: "${OUTPUT_DIR:?OUTPUT_DIR is required}"
NAMESPACE="${NAMESPACE:-prontuario-homolog}"
AUTH_JWT_SECRET="${AUTH_JWT_SECRET:-change-me-dev-secret}"
INGRESS_HOST="${INGRESS_HOST:-homolog.prontuario.local}"

mkdir -p "${OUTPUT_DIR}"

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

cat > "${OUTPUT_DIR}/00-namespace.yaml" <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
---
apiVersion: v1
kind: Secret
metadata:
  name: auth-secrets
  namespace: ${NAMESPACE}
type: Opaque
stringData:
  AUTH_JWT_SECRET: ${AUTH_JWT_SECRET}
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: service-endpoints
  namespace: ${NAMESPACE}
data:
  AUTH_SERVICE_URL: http://auth-service:8000
  PATIENT_SERVICE_URL: http://patient-service:8000
  EMR_SERVICE_URL: http://emr-service:8000
  SCHEDULING_SERVICE_URL: http://scheduling-service:8000
  AUDIT_SERVICE_URL: http://audit-service:8000
  PROFESSIONAL_SERVICE_URL: http://professional-service:8000
EOF

for trace_file in "${trace_files[@]}"; do
  service="$(read_trace_field "${trace_file}" service)"
  repository="$(read_trace_field "${trace_file}" repository)"
  digest="$(read_trace_field "${trace_file}" digest)"

  if [ -z "${service}" ] || [ -z "${repository}" ] || [ -z "${digest}" ] || [ "${digest}" = "null" ]; then
    echo "Invalid trace metadata in ${trace_file}" >&2
    exit 1
  fi

  db_name="${service%-service}"
  image_ref="${repository}@${digest}"
  replicas=1
  if [ "${service}" = "auth-service" ] || [ "${service}" = "gateway-service" ] || [ "${service}" = "patient-service" ]; then
    replicas=2
  fi

  cat >> "${OUTPUT_DIR}/10-services.yaml" <<EOF
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${service}
  namespace: ${NAMESPACE}
  labels:
    app: ${service}
spec:
  replicas: ${replicas}
  selector:
    matchLabels:
      app: ${service}
  template:
    metadata:
      labels:
        app: ${service}
    spec:
      containers:
      - name: ${service}
        image: ${image_ref}
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 3
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 20
          periodSeconds: 20
          timeoutSeconds: 3
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        volumeMounts:
        - name: data
          mountPath: /app/data
        env:
        - name: APP_ENV
          value: homolog
EOF

  case "${service}" in
    auth-service)
      cat >> "${OUTPUT_DIR}/10-services.yaml" <<EOF
        - name: AUTH_DATABASE_URL
          value: sqlite:////app/data/auth.db
        - name: AUTH_JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: auth-secrets
              key: AUTH_JWT_SECRET
EOF
      ;;
    patient-service)
      cat >> "${OUTPUT_DIR}/10-services.yaml" <<EOF
        - name: AUTH_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUTH_SERVICE_URL
        - name: AUDIT_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUDIT_SERVICE_URL
        - name: PATIENT_DATABASE_URL
          value: sqlite:////app/data/patient.db
EOF
      ;;
    emr-service)
      cat >> "${OUTPUT_DIR}/10-services.yaml" <<EOF
        - name: AUTH_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUTH_SERVICE_URL
        - name: AUDIT_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUDIT_SERVICE_URL
        - name: EMR_DATABASE_URL
          value: sqlite:////app/data/emr.db
EOF
      ;;
    scheduling-service)
      cat >> "${OUTPUT_DIR}/10-services.yaml" <<EOF
        - name: AUTH_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUTH_SERVICE_URL
        - name: SCHEDULING_DATABASE_URL
          value: sqlite:////app/data/scheduling.db
EOF
      ;;
    audit-service)
      cat >> "${OUTPUT_DIR}/10-services.yaml" <<EOF
        - name: AUTH_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUTH_SERVICE_URL
        - name: AUDIT_DATABASE_URL
          value: sqlite:////app/data/audit.db
EOF
      ;;
    professional-service)
      cat >> "${OUTPUT_DIR}/10-services.yaml" <<EOF
        - name: AUTH_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUTH_SERVICE_URL
        - name: AUDIT_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUDIT_SERVICE_URL
        - name: PROFESSIONAL_DATABASE_URL
          value: sqlite:////app/data/professional.db
EOF
      ;;
    gateway-service)
      cat >> "${OUTPUT_DIR}/10-services.yaml" <<EOF
        - name: AUTH_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUTH_SERVICE_URL
        - name: PATIENT_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: PATIENT_SERVICE_URL
        - name: EMR_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: EMR_SERVICE_URL
        - name: SCHEDULING_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: SCHEDULING_SERVICE_URL
        - name: AUDIT_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: AUDIT_SERVICE_URL
        - name: PROFESSIONAL_SERVICE_URL
          valueFrom:
            configMapKeyRef:
              name: service-endpoints
              key: PROFESSIONAL_SERVICE_URL
EOF
      ;;
    *)
      echo "Unsupported service in trace: ${service}" >&2
      exit 1
      ;;
  esac

  cat >> "${OUTPUT_DIR}/10-services.yaml" <<EOF
      volumes:
      - name: data
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: ${service}
  namespace: ${NAMESPACE}
  labels:
    app: ${service}
spec:
  selector:
    app: ${service}
  ports:
  - name: http
    port: 8000
    targetPort: 8000
EOF

done

cat > "${OUTPUT_DIR}/20-ingress.yaml" <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gateway-ingress
  namespace: ${NAMESPACE}
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
  - host: ${INGRESS_HOST}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: gateway-service
            port:
              number: 8000
EOF

cat > "${OUTPUT_DIR}/30-resilience.yaml" <<EOF
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-service-hpa
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: auth-service
  minReplicas: 2
  maxReplicas: 4
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: patient-service-hpa
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: patient-service
  minReplicas: 2
  maxReplicas: 4
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gateway-service-hpa
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gateway-service
  minReplicas: 2
  maxReplicas: 4
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: auth-service-pdb
  namespace: ${NAMESPACE}
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: auth-service
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: patient-service-pdb
  namespace: ${NAMESPACE}
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: patient-service
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: gateway-service-pdb
  namespace: ${NAMESPACE}
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: gateway-service
EOF

echo "Rendered manifests in ${OUTPUT_DIR}"
