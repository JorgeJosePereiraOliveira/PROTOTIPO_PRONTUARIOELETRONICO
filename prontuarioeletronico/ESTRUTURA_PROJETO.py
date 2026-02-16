"""
ESTRUTURA COMPLETA DO PROJETO - Prontuário Eletrônico em Clean Architecture
Gerado automaticamente pela estrutura de diretórios
"""

STRUCTURE = """
prontuarioeletronico/
│
├── README.md                          ← Documentação principal
├── ARQUITETURA_DETALHES.py           ← Documento de arquitetura
├── EXEMPLOS_USO.sh                   ← Exemplos de requisições API
│
├── requirements.txt                   ← Dependências Python
├── Dockerfile                         ← Imagem Docker
├── docker-compose.yaml                ← Orquestração local
│
├── quickstart.sh                      ← Quick start (Linux/Mac)
├── quickstart.bat                     ← Quick start (Windows)
│
├── tests.py                           ← Testes unitários
│
│
├── src/                               ← CÓDIGO FONTE
│
│   ├── __init__.py
│   │
│   ├── domain/                        ← CAMADA 1: ENTIDADES (Núcleo)
│   │   ├── __init__.py
│   │   │
│   │   ├── __seedwork/               ← Base classes
│   │   │   ├── __init__.py
│   │   │   ├── entity.py             ← Entity (base)
│   │   │   ├── use_case_interface.py ← UseCase<InputDTO, OutputDTO>
│   │   │   └── repository_interface.py ← RepositoryInterface<T>
│   │   │
│   │   ├── patient/                  ← Paciente
│   │   │   ├── __init__.py
│   │   │   ├── patient_entity.py     ← Patient (entidade)
│   │   │   └── patient_repository_interface.py
│   │   │
│   │   ├── professional/             ← Profissional de Saúde
│   │   │   ├── __init__.py
│   │   │   ├── professional_entity.py ← Professional (entidade)
│   │   │   └── professional_repository_interface.py
│   │   │
│   │   ├── clinical_record/          ← Registro Clínico (RCOP/SOAP)
│   │   │   ├── __init__.py
│   │   │   ├── rcop_soap.py          ← Problem, ClinicalRecord, Subjective, Objective, Assessment, Plan
│   │   │   └── clinical_record_repository_interface.py
│   │   │
│   │   └── appointment/              ← Consulta/Agendamento
│   │       ├── __init__.py
│   │       ├── appointment_entity.py ← Appointment (entidade)
│   │       └── appointment_repository_interface.py
│   │
│   ├── application/                  ← CAMADA 2: CASOS DE USO
│   │   ├── __init__.py
│   │   │
│   │   ├── patient/                  ← Casos de uso de paciente
│   │   │   ├── __init__.py
│   │   │   └── register_patient_usecase.py
│   │   │
│   │   ├── clinical_record/          ← Casos de uso de registro clínico
│   │   │   ├── __init__.py
│   │   │   ├── register_soap_usecase.py
│   │   │   └── create_problem_usecase.py
│   │   │
│   │   └── appointment/              ← Casos de uso de consulta
│   │       ├── __init__.py
│   │       └── schedule_appointment_usecase.py
│   │
│   └── infra/                        ← CAMADAS 3 & 4: ADAPTADORES & DRIVERS
│       ├── __init__.py
│       │
│       ├── api/                      ← CAMADA 3: API REST (Controllers/Presenters)
│       │   ├── __init__.py
│       │   ├── main.py               ← FastAPI app
│       │   ├── config.py             ← Configuração FastAPI
│       │   ├── database.py           ← Configuração SQLAlchemy
│       │   │
│       │   ├── routers/              ← Controllers
│       │   │   ├── __init__.py
│       │   │   ├── patient_routers.py        ← Endpoints /api/v1/patients
│       │   │   └── clinical_record_routers.py ← Endpoints /api/v1/clinical-records
│       │   │
│       │   └── presenters/           ← DTOs de API
│       │       ├── __init__.py
│       │       ├── patient_presenter.py           ← PatientCreateRequest, PatientResponse
│       │       └── clinical_record_presenter.py   ← RegisterSOAPRequest, CreateProblemRequest
│       │
│       ├── patient/                 ← CAMADA 4: Persistência de Paciente
│       │   └── sqlalchemy/
│       │       ├── __init__.py
│       │       ├── patient_model.py       ← Modelo ORM
│       │       └── patient_repository.py  ← Implementação repositório
│       │
│       ├── clinical_record/         ← CAMADA 4: Persistência de Registro Clínico
│       │   └── sqlalchemy/
│       │       ├── __init__.py
│       │       ├── clinical_record_model.py       ← Modelos ORM (ClinicalRecord, Problem, SOAP)
│       │       └── clinical_record_repository.py  ← Implementação repositório
│       │
│       └── appointment/             ← CAMADA 4: Persistência de Consulta
│           └── sqlalchemy/
│               ├── __init__.py
│               ├── appointment_model.py       ← Modelo ORM
│               └── appointment_repository.py  ← Implementação repositório
│
└── [Database files created at runtime]
    └── prontuario.db                ← SQLite database


═════════════════════════════════════════════════════════════════════════════
MAPEAMENTO: CLEAN ARCHITECTURE → ESTRUTURA FÍSICA
═════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│ CAMADA 1: ENTIDADES (Domain Layer)                                      │
│ Localização: src/domain/**/*_entity.py                                  │
│ Exemplo: src/domain/patient/patient_entity.py                           │
│ Dependências: NENHUMA (apenas stdlib Python)                            │
│ Função: Encapsular regras de negócio corporativas (RCOP/SOAP)          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ CAMADA 2: CASOS DE USO (Application Layer)                              │
│ Localização: src/application/**/*_usecase.py                            │
│ Exemplo: src/application/patient/register_patient_usecase.py            │
│ Dependências: Domain layer + RepositoryInterface (abstração)           │
│ Função: Orquestrar fluxo de negócio (regras da aplicação)             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ CAMADA 3: ADAPTADORES (Interface Adapters Layer)                        │
│ A. Controllers: src/infra/api/routers/*_routers.py                     │
│ B. Presenters/DTOs: src/infra/api/presenters/*_presenter.py            │
│ Dependências: Application + Domain + Pydantic + FastAPI                │
│ Função: Converter HTTP ↔ Use Case ↔ Response                           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ CAMADA 4: FRAMEWORKS & DRIVERS (External Details)                       │
│ A. Models ORM: src/infra/*/sqlalchemy/*_model.py                       │
│ B. Repositories: src/infra/*/sqlalchemy/*_repository.py                │
│ C. Config: src/infra/api/config.py, database.py, main.py              │
│ Dependências: Tudo (SQLAlchemy, FastAPI, banco de dados)              │
│ Função: Detalhes técnicos (persistência, framework, etc.)             │
└─────────────────────────────────────────────────────────────────────────┘


═════════════════════════════════════════════════════════════════════════════
REGRA DA DEPENDÊNCIA
═════════════════════════════════════════════════════════════════════════════

✓ FLUXO CORRETO (Dependências apontam para o centro):
  src/infra/*_repository.py → src/domain/*_entity.py
  src/application/*_usecase.py → src/domain/*_entity.py
  src/infra/api/routers/*_routers.py → src/application/*_usecase.py

✗ NUNCA O CONTRÁRIO:
  src/domain/*_entity.py X→ src/application/
  src/domain/*_entity.py X→ src/infra/
  Entities NUNCA conhecem camadas externas!


═════════════════════════════════════════════════════════════════════════════
FLUXO DE UMA REQUISIÇÃO HTTP
═════════════════════════════════════════════════════════════════════════════

REQUEST HTTP
    ↓ JSON
[src/infra/api/main.py] FastAPI App
    ↓
[src/infra/api/routers/patient_routers.py] Router
    ↓ Pydantic validates
[src/infra/api/presenters/patient_presenter.py] PatientCreateRequest
    ↓
create_patient(request: PatientCreateRequest)
    ↓
[src/application/patient/register_patient_usecase.py] RegisterPatientUseCase
    ↓
RegisterPatientUseCase(repository).execute(input_dto)
    ↓
[src/domain/patient/patient_entity.py] Patient entity
    ↓
repository.add(patient)
    ↓
[src/infra/patient/sqlalchemy/patient_repository.py] PatientRepository
    ↓
[src/infra/patient/sqlalchemy/patient_model.py] PatientModel
    ↓ SQLAlchemy
[Database] INSERT INTO patients...
    ↓
COMMIT
    ↓ OutputDTO
[src/application/patient/register_patient_usecase.py] RegisterPatientOutputDTO
    ↓
Router formats response
    ↓
[src/infra/api/presenters/patient_presenter.py] JSON
    ↓
RESPONSE HTTP 200 OK
    ↓ Application/JSON
{
  "patient_id": "uuid-xxxx",
  "message": "Patient registered successfully"
}


═════════════════════════════════════════════════════════════════════════════
TABELAS DE BANCO DE DADOS
═════════════════════════════════════════════════════════════════════════════

Tabelas Principais:
├── patients               ← Dados de paciente
├── professionals          ← Dados de profissional
├── appointments           ← Agendamentos
│
└── clinical_records       ← Registro clínico (cabeçalho)
    ├── problems           ← Problemas clínicos (RCOP)
    │
    └── SOAP Components:
        ├── soap_subjectives    ← S: Dados subjetivos
        ├── soap_objectives     ← O: Dados objetivos
        ├── soap_assessments    ← A: Avaliação
        └── soap_plans          ← P: Plano


═════════════════════════════════════════════════════════════════════════════
TECNOLOGIAS POR CAMADA
═════════════════════════════════════════════════════════════════════════════

Domain [src/domain/]
  Language: Python 3.10+
  Dependencies: None (stdlib only)
  Framework: None
  Purpose: Pure business logic

Application [src/application/]
  Language: Python 3.10+
  Dependencies: Domain layer
  Framework: None
  Additional: Pydantic for DTOs

Infrastructure [src/infra/]
  API Layer:
    Framework: FastAPI
    Server: Uvicorn
    Validation: Pydantic
  Persistence Layer:
    ORM: SQLAlchemy 2.0
    Database: SQLite (dev), PostgreSQL (prod)
  Containerization:
    Docker
    Docker Compose


═════════════════════════════════════════════════════════════════════════════
COMO EXECUTAR
═════════════════════════════════════════════════════════════════════════════

1. Installation & Development:
   $ cd prontuarioeletronico
   $ python -m venv venv
   $ source venv/bin/activate  # ou venv\\Scripts\\activate no Windows
   $ pip install -r requirements.txt
   $ python -m pytest tests.py -v
   $ python -m uvicorn src.infra.api.main:app --reload

2. Docker:
   $ docker-compose up --build
   $ curl http://localhost:8000/api/v1


═════════════════════════════════════════════════════════════════════════════
PRÓXIMAS ETAPAS
═════════════════════════════════════════════════════════════════════════════

1. Autenticação & Autorização
   - JWT tokens
   - Role-based access (médico, admin, enfermeira)

2. Mais Casos de Uso
   - UpdatePatient
   - FindPatientByID
   - SearchRecordsByProblem
   - EvolutionHistory

3. Validação Clínica Avançada
   - Regras RCOP/SOAP customizadas
   - Alertas de segurança

4. Integração com IA
   - Sugestão diagnóstica
   - Análise de risco
   - MLOps integration

5. Auditoria & Compliance
   - Audit logging
   - LGPD compliance
   - Criptografia de dados sensíveis

6. Qualidade de Código
   - Coverage > 80%
   - CI/CD pipeline
   - Documentação Sphinx
   - Type hints com mypy

7. Escalabilidade
   - Redis cache
   - Elasticsearch
   - API Gateway
   - Kubernetes deployment

════════════════════════════════════════════════════════════════════════════
"""

print(STRUCTURE)
