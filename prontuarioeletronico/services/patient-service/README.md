# Patient Service

Microsserviço de pacientes (MS-02 / US-2.2) em Clean Architecture.

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

## Endpoints (fase 1)

- `GET /health` -> liveness/readiness
- `GET /api/v1/info` -> metadados do serviço
- `POST /api/v1/patients` -> criar paciente
- `GET /api/v1/patients/{patient_id}` -> buscar paciente
- `GET /api/v1/patients` -> listar pacientes

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
