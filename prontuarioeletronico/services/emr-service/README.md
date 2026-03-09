# Emr Service

Microsserviço gerado a partir do template ARC-02 com Clean Architecture por contexto.

## Estrutura

```text
emr-service/
├── src/
│   └── emr/
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
uvicorn src.emr.infra.api.main:app --reload --port 8003
```

## Variaveis de ambiente

- `APP_ENV` (default: `development`)
- `AUTH_SERVICE_URL` (default: `http://localhost:8001` fora de prod/staging)
- `EMR_DATABASE_URL` (default: `sqlite:///./emr.db`)

## Endpoints

- `GET /health` -> liveness/readiness
- `GET /api/v1/info` -> metadados do serviço
- `POST /api/v1/emr/problems` -> cria problema RCOP
- `GET /api/v1/emr/problems/{problem_id}` -> busca problema RCOP
- `POST /api/v1/emr/soap` -> cria registro SOAP
- `GET /api/v1/emr/soap/{soap_id}` -> busca registro SOAP
