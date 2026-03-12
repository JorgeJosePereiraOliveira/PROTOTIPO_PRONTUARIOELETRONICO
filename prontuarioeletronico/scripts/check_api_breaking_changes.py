import importlib
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "contracts" / "api_compatibility_baseline.json"

SERVICES = {
    "auth-service": {
        "service_root": ROOT / "services" / "auth-service",
        "import_path": "src.auth.infra.api.main",
        "env": {
            "APP_ENV": "test",
            "AUTH_JWT_SECRET": "compatibility-check-secret",
            "AUTH_DATABASE_URL": "sqlite:///./test_auth_compat.db",
        },
    },
    "patient-service": {
        "service_root": ROOT / "services" / "patient-service",
        "import_path": "src.patient.infra.api.main",
        "env": {
            "APP_ENV": "test",
            "PATIENT_DATABASE_URL": "sqlite:///./test_patient_compat.db",
            "AUTH_SERVICE_URL": "http://localhost:8001",
        },
    },
    "gateway-service": {
        "service_root": ROOT / "services" / "gateway-service",
        "import_path": "src.gateway.infra.api.main",
        "env": {
            "APP_ENV": "test",
            "AUTH_SERVICE_URL": "http://localhost:8001",
            "PATIENT_SERVICE_URL": "http://localhost:8002",
            "EMR_SERVICE_URL": "http://localhost:8003",
            "SCHEDULING_SERVICE_URL": "http://localhost:8004",
            "AUDIT_SERVICE_URL": "http://localhost:8005",
            "PROFESSIONAL_SERVICE_URL": "http://localhost:8006",
        },
    },
    "emr-service": {
        "service_root": ROOT / "services" / "emr-service",
        "import_path": "src.emr.infra.api.main",
        "env": {
            "APP_ENV": "test",
            "EMR_DATABASE_URL": "sqlite:///./test_emr_compat.db",
            "AUTH_SERVICE_URL": "http://localhost:8001",
        },
    },
    "scheduling-service": {
        "service_root": ROOT / "services" / "scheduling-service",
        "import_path": "src.scheduling.infra.api.main",
        "env": {
            "APP_ENV": "test",
            "SCHEDULING_DATABASE_URL": "sqlite:///./test_scheduling_compat.db",
            "AUTH_SERVICE_URL": "http://localhost:8001",
        },
    },
    "audit-service": {
        "service_root": ROOT / "services" / "audit-service",
        "import_path": "src.audit.infra.api.main",
        "env": {
            "APP_ENV": "test",
            "AUDIT_DATABASE_URL": "sqlite:///./test_audit_compat.db",
            "AUTH_SERVICE_URL": "http://localhost:8001",
        },
    },
    "professional-service": {
        "service_root": ROOT / "services" / "professional-service",
        "import_path": "src.professional.infra.api.main",
        "env": {
            "APP_ENV": "test",
            "PROFESSIONAL_DATABASE_URL": "sqlite:///./test_professional_compat.db",
            "AUTH_SERVICE_URL": "http://localhost:8001",
            "AUDIT_SERVICE_URL": "http://localhost:8005",
        },
    },
}


def _load_baseline() -> dict[str, set[str]]:
    with BASELINE_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return {key: set(value) for key, value in data.items()}


def _extract_operations(spec: dict) -> set[str]:
    operations: set[str] = set()
    for path, methods in spec.get("paths", {}).items():
        for method in methods.keys():
            operations.add(f"{method.upper()} {path}")
    return operations


def _load_openapi_operations(service_name: str, config: dict) -> set[str]:
    for env_key, env_value in config["env"].items():
        os.environ.setdefault(env_key, env_value)

    service_root = str(config["service_root"])
    if service_root not in sys.path:
        sys.path.insert(0, service_root)

    module = importlib.import_module(config["import_path"])
    app = getattr(module, "app")
    return _extract_operations(app.openapi())


def main() -> int:
    baseline = _load_baseline()

    failures: list[str] = []
    for service_name, config in SERVICES.items():
        current = _load_openapi_operations(service_name, config)
        expected = baseline.get(service_name, set())

        missing = sorted(expected - current)
        if missing:
            failures.append(
                f"[{service_name}] breaking change detected; missing operations: {', '.join(missing)}"
            )

    if failures:
        print("API compatibility check failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("API compatibility check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
