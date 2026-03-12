# Professional Service

Microsservico de profissionais (MS-06) em Clean Architecture.

Persistencia principal via SQLAlchemy.

## Estrutura

```text
professional-service/
├── src/
│   └── professional/
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
uvicorn src.professional.infra.api.main:app --reload --port 8001
```

## Endpoints (fase 1)

- `GET /health` -> liveness/readiness
- `GET /api/v1/info` -> metadados do servico
- `POST /api/v1/professionals` -> registrar profissional
- `GET /api/v1/professionals/{professional_id}` -> buscar profissional
- `GET /api/v1/professionals` -> listar profissionais
- `POST /api/v1/professionals/{professional_id}/activate` -> ativar profissional
- `POST /api/v1/professionals/{professional_id}/deactivate` -> desativar profissional

## Seguranca JWT/RBAC (integracao com auth-service)

- Endpoints exigem `Authorization: Bearer <token>`.
- Integracao com auth-service por HTTP em:
	- `GET /api/v1/auth/verify`
	- `GET /api/v1/auth/authorize?required_role=<role>`
- Regras de acesso:
	- create/activate/deactivate: `admin`
	- get/list: `admin` ou `profissional`

Configuracao:

- `AUTH_SERVICE_URL` (default: `http://localhost:8001`)
- `AUDIT_SERVICE_URL` (default: `http://localhost:8005`)
- `PROFESSIONAL_DATABASE_URL` (default: `sqlite:///./professional.db`)

Hardening SEC-01:

- Em `production`/`staging`, as variaveis obrigatorias devem estar definidas.
- Arquivo de referencia: `.env.example`

## Regras de validacao (fase 1)

- `full_name` com minimo de 3 caracteres
- `document_cpf` com 11 digitos numericos
- `council_uf` com 2 letras
- unicidade de `council_type + council_uf + council_number`
- status inicial `active`
- ativar/desativar idempotente

## Testes

```bash
pytest -q
```

Principais arquivos de teste:

- `tests/test_professional_api.py`
- `tests/test_openapi_contract.py`
- `tests/test_authorization_e2e.py` (integracao E2E com token real do auth-service, sem mock)
