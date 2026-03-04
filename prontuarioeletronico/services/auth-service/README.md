# Auth Service

Microsserviço de autenticação e autorização (JWT + RBAC) iniciado a partir do template ARC-02.

Persistência de usuários via SQLAlchemy.
Hardening de senha com `passlib` + `bcrypt`.

## Estrutura

```text
auth-service/
├── src/
│   └── auth/
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
uvicorn src.auth.infra.api.main:app --reload --port 8001
```

## Endpoints

- `GET /health` -> liveness/readiness
- `GET /api/v1/info` -> metadados do serviço
- `POST /api/v1/auth/login` -> autenticação e emissão de JWT
- `GET /api/v1/auth/verify` -> validação de JWT
- `GET /api/v1/auth/authorize?required_role=<role>` -> autorização RBAC

## Usuários de bootstrap (dev)

- admin / admin123 (role: admin)
- profissional / prof123 (role: profissional)

## Configuração

- `AUTH_JWT_SECRET` (**obrigatória em todos os ambientes**)
- `APP_ENV` (opcional, default: `development`)
- `AUTH_DATABASE_URL` (opcional)
	- padrão: `sqlite:///./auth.db`
