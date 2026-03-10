# Scheduling Service

Microsserviço gerado a partir do template ARC-02 com Clean Architecture por contexto.

## Estrutura

```text
scheduling-service/
├── src/
│   └── scheduling/
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
uvicorn src.scheduling.infra.api.main:app --reload --port 8004
```

## Variaveis de ambiente

- `APP_ENV` (default: `development`)
- `AUTH_SERVICE_URL` (default: `http://localhost:8001` fora de prod/staging)
- `SCHEDULING_DATABASE_URL` (default: `sqlite:///./scheduling.db`)

## Endpoints

- `GET /health` -> liveness/readiness
- `GET /api/v1/info` -> metadados do serviço
- `POST /api/v1/scheduling/appointments` -> cria agendamento
- `GET /api/v1/scheduling/appointments/{appointment_id}` -> busca agendamento por id
- `GET /api/v1/scheduling/appointments` -> lista agendamentos
- `DELETE /api/v1/scheduling/appointments/{appointment_id}` -> remove agendamento
