# Gateway Service

API Gateway para roteamento integrado de `auth-service` e `patient-service`.

## Estrutura

```text
gateway-service/
├── src/
│   └── gateway/
│       ├── domain/
│       ├── application/
│       └── infra/
├── tests/
├── requirements.txt
├── run_tests.py
└── Dockerfile
```

## Executar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
uvicorn src.gateway.infra.api.main:app --reload --port 8001
```

## Endpoints base

- `GET /health` -> liveness/readiness
- `GET /api/v1/info` -> metadados do serviço

## Endpoints proxy (Auth)

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/verify`
- `GET /api/v1/auth/authorize`

## Endpoints proxy (Patient)

- `POST /api/v1/patients`
- `GET /api/v1/patients`
- `GET /api/v1/patients/{patient_id}`
- `PUT /api/v1/patients/{patient_id}`
- `DELETE /api/v1/patients/{patient_id}`

## Configuração

- `AUTH_SERVICE_URL` (default: `http://localhost:8001`)
- `PATIENT_SERVICE_URL` (default: `http://localhost:8002`)

## Testes

```bash
pytest -q
```

Principais suítes:

- `tests/test_gateway_integration.py` (integração real gateway+auth+patient)
- `tests/test_gateway_openapi_contract.py` (contrato OpenAPI do gateway)
