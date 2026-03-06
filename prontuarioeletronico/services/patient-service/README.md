# Patient Service

Microsserviço de pacientes (MS-02 / US-2.2) em Clean Architecture.

Persistência principal via SQLAlchemy.

## Estrutura

```text
patient-service/
├── src/
│   └── patient/
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
uvicorn src.patient.infra.api.main:app --reload --port 8001
```

## Endpoints (fase 2)

- `GET /health` -> liveness/readiness
- `GET /api/v1/info` -> metadados do serviço
- `POST /api/v1/patients` -> criar paciente
- `GET /api/v1/patients/{patient_id}` -> buscar paciente
- `GET /api/v1/patients` -> listar pacientes
- `PUT /api/v1/patients/{patient_id}` -> atualizar paciente
- `DELETE /api/v1/patients/{patient_id}` -> remover paciente

## Segurança JWT/RBAC (integração com auth-service)

- Endpoints de paciente exigem `Authorization: Bearer <token>`.
- Integração com auth-service por HTTP em:
	- `GET /api/v1/auth/verify`
	- `GET /api/v1/auth/authorize?required_role=<role>`
- Regras de acesso:
	- create/get/list/update: `admin` ou `profissional`
	- delete: `admin`

Configuração:

- `AUTH_SERVICE_URL` (default: `http://localhost:8001`)
- `PATIENT_DATABASE_URL` (default: `sqlite:///./patient.db`)

Hardening SEC-01:

- Em `production`/`staging`, `AUTH_SERVICE_URL` e `PATIENT_DATABASE_URL` são obrigatórios.
- Arquivo de referência: `.env.example`

## Regras de validação (fase 1)

- `name` com mínimo de 3 caracteres
- `cpf` com 11 dígitos numéricos
- `gender` em `M`, `F`, `O` ou `N`
- `cpf` único no repositório

## Testes

```bash
pytest -q
```

Principais arquivos de teste:

- `tests/test_patient_api.py`
- `tests/test_openapi_contract.py`
- `tests/test_authorization_e2e.py` (integração E2E com token real do auth-service, sem mock)
