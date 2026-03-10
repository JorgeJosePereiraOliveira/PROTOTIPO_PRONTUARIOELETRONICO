# Audit Service

Microsservico de auditoria para registro de eventos criticos por usuario/operacao.

## Executar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
uvicorn src.audit.infra.api.main:app --reload --port 8005
```

## Variaveis de ambiente

- `APP_ENV` (default: `development`)
- `AUTH_SERVICE_URL` (default: `http://localhost:8001` fora de prod/staging)
- `AUDIT_DATABASE_URL` (default: `sqlite:///./audit.db`)

## Endpoints

- `GET /health`
- `GET /api/v1/info`
- `POST /api/v1/audit/events`
- `GET /api/v1/audit/events`
- `GET /api/v1/audit/events/{event_id}`
