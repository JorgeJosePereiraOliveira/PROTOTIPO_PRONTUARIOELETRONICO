  
FILE_TREE = """

╔═══════════════════════════════════════════════════════════════════════════╗
║                    PRONTUÁRIO ELETRÔNICO - ESTRUTURA                      ║
║                    Clean Architecture Implementation                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

prontuarioeletronico/
│
├─ 📄 README.md                        Principal documentation
├─ 📄 GUIA_RAPIDO.md                   Quick reference guide
├─ 📄 ESTRUTURA_PROJETO.py             Project structure details
├─ 📄 ARQUITETURA_DETALHES.py          In-depth architecture documentation
├─ 📄 EXEMPLOS_USO.sh                  Usage examples (cURL)
│
├─ ⚙️ Configuration Files
│  ├─ requirements.txt                 Python dependencies
│  ├─ Dockerfile                       Container image
│  ├─ docker-compose.yaml              Local orchestration
│  └─ quickstart.sh / .bat             Quick start scripts
│
├─ 🧪 tests.py                         Unit tests
│
│
└─ 📁 src/                             SOURCE CODE
   │
   ├─ 📁 domain/                       ━━━ LAYER 1: ENTITIES ━━━━━━━━━━━━━━━
   │  │  ✓ No external dependencies
   │  │  ✓ Pure business logic
   │  │  ✓ RCOP/SOAP core
   │  │
   │  ├─ 📁 __seedwork/
   │  │  ├─ entity.py                  Base Entity class
   │  │  ├─ use_case_interface.py      UseCase<Input, Output> abstract
   │  │  └─ repository_interface.py    Repository<T> abstract
   │  │
   │  ├─ 📁 patient/
   │  │  ├─ __init__.py
   │  │  ├─ patient_entity.py          💎 Patient entity
   │  │  └─ patient_repository_interface.py
   │  │
   │  ├─ 📁 professional/
   │  │  ├─ __init__.py
   │  │  ├─ professional_entity.py     💎 Professional entity
   │  │  └─ professional_repository_interface.py
   │  │
   │  ├─ 📁 clinical_record/
   │  │  ├─ __init__.py
   │  │  ├─ rcop_soap.py               💎 Problem, ClinicalRecord, SOAP components
   │  │  └─ clinical_record_repository_interface.py
   │  │
   │  └─ 📁 appointment/
   │     ├─ __init__.py
   │     ├─ appointment_entity.py      💎 Appointment entity
   │     └─ appointment_repository_interface.py
   │
   │
   ├─ 📁 application/                  ━━━ LAYER 2: USE CASES ━━━━━━━━━━━━
   │  │  ✓ Application-specific rules
   │  │  ✓ Orchestrates entities
   │  │  ✓ Depends on Domain only
   │  │
   │  ├─ 📁 patient/
   │  │  ├─ __init__.py
   │  │  └─ register_patient_usecase.py
   │  │     └─ Input: RegisterPatientDTO
   │  │     └─ Output: RegisterPatientOutputDTO
   │  │
   │  ├─ 📁 clinical_record/
   │  │  ├─ __init__.py
   │  │  ├─ register_soap_usecase.py
   │  │  │  └─ Input: RegisterSOAPDTO
   │  │  │  └─ Output: RegisterSOAPOutputDTO
   │  │  └─ create_problem_usecase.py
   │  │     └─ Input: CreateProblemDTO
   │  │     └─ Output: CreateProblemOutputDTO
   │  │
   │  └─ 📁 appointment/
   │     ├─ __init__.py
   │     └─ schedule_appointment_usecase.py
   │        └─ Input: ScheduleAppointmentDTO
   │        └─ Output: ScheduleAppointmentOutputDTO
   │
   │
   └─ 📁 infra/                        ━━━ LAYERS 3 & 4: ADAPTERS & DRIVERS
      │  Layer 3: Web framework (HTTP handlers)
      │  Layer 4: Persistence (DB implementations)
      │
      ├─ 📁 api/                       [LAYER 3: Interface Adapters]
      │  │  ✓ HTTP endpoints
      │  │  ✓ Request/Response handling
      │  │  ✓ Pydantic validation
      │  │
      │  ├─ __init__.py
      │  ├─ main.py                     FastAPI app with routers
      │  ├─ config.py                   FastAPI configuration
      │  ├─ database.py                 SQLAlchemy session factory
      │  │
      │  ├─ 📁 routers/                 [Controllers]
      │  │  ├─ __init__.py
      │  │  ├─ patient_routers.py
      │  │  │  ├─ POST   /api/v1/patients/
      │  │  │  ├─ GET    /api/v1/patients/{id}
      │  │  │  └─ GET    /api/v1/patients/
      │  │  │
      │  │  └─ clinical_record_routers.py
      │  │     ├─ POST   /api/v1/clinical-records/problems
      │  │     └─ POST   /api/v1/clinical-records/soap
      │  │
      │  └─ 📁 presenters/              [DTOs & Validation]
      │     ├─ __init__.py
      │     ├─ patient_presenter.py
      │     │  ├─ PatientCreateRequest
      │     │  └─ PatientResponse
      │     │
      │     └─ clinical_record_presenter.py
      │        ├─ RegisterSOAPRequest
      │        ├─ CreateProblemRequest
      │        └─ ClinicalRecordResponse
      │
      ├─ 📁 patient/                   [LAYER 4: Persistence]
      │  └─ 📁 sqlalchemy/
      │     ├─ __init__.py
      │     ├─ patient_model.py         PatientModel (SQLAlchemy ORM)
      │     └─ patient_repository.py    PatientRepository (implementation)
      │
      ├─ 📁 clinical_record/          [LAYER 4: Persistence]
      │  └─ 📁 sqlalchemy/
      │     ├─ __init__.py
      │     ├─ clinical_record_model.py
      │     │  ├─ ClinicalRecordModel
      │     │  ├─ ProblemModel
      │     │  ├─ SubjectiveModel
      │     │  ├─ ObjectiveModel
      │     │  ├─ AssessmentModel
      │     │  └─ PlanModel
      │     │
      │     └─ clinical_record_repository.py (implementation)
      │
      └─ 📁 appointment/              [LAYER 4: Persistence]
         └─ 📁 sqlalchemy/
            ├─ __init__.py
            ├─ appointment_model.py     AppointmentModel (SQLAlchemy ORM)
            └─ appointment_repository.py (implementation)


═══════════════════════════════════════════════════════════════════════════════

LEGEND:
  📁  directory
  📄  documentation file
  ⚙️   configuration file
  🧪  testing
  💎  Core entity (business logic)
  →   imports from
  ✓   characteristic

═══════════════════════════════════════════════════════════════════════════════

DEPENDENCY FLOW (correct → ):

┌─────────────────────────────────────┐
│ src/infra/api/routers/              │  HTTP Request Handler
│ (FastAPI Controller)                │
│ patient_routers.py                  │
└────────────────────┬────────────────┘
                     → imports from
                     ↓
  ┌──────────────────────────────────────────┐
  │ src/infra/api/presenters/                │  Request Validation
  │ (Pydantic DTOs)                          │
  │ patient_presenter.py                     │
  └──────────────────────┬───────────────────┘
                         → imports from
                         ↓
    ┌────────────────────────────────────────────────┐
    │ src/application/patient/                       │  Use Case Layer
    │ register_patient_usecase.py                    │
    │ (Business logic orchestration)                │
    └──────────────────────┬───────────────────────┘
                           → imports from
                           ↓
        ┌──────────────────────────────────────────────┐
        │ src/domain/patient/                          │  Entity Layer
        │ patient_entity.py                            │  (CORE - No deps)
        │ (Pure business rules)                        │
        └──────────────────────┬───────────────────────┘
                               → imports from
                               ↓
            ┌────────────────────────────────────────────────────┐
            │ src/domain/__seedwork/                             │
            │ (Base classes for architecture)                    │
            └────────────────────────────────────────────────────┘

And separately:

┌─────────────────────────────────────────────────────┐
│ src/infra/patient/sqlalchemy/                       │  Persistence Detail
│ patient_repository.py                               │  (converts DB ↔ Entity)
│ (Implements RepositoryInterface from domain)        │
└──────────────────────────────────────────────────────┘
        ↓ reads/writes
┌──────────────────────────────────────────────────────┐
│ src/infra/patient/sqlalchemy/                        │
│ patient_model.py                                     │
│ (SQLAlchemy ORM Model)                               │
└──────────────────────────────────────────────────────┘
        ↓ ORM generated SQL
┌──────────────────────────────────────────────────────┐
│ SQL Database                                         │
│ (SQLite / PostgreSQL)                                │
└──────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

FILE STATISTICS:

Domain Layer (src/domain/):
  - ~600 lines  | 6 entity files
  - Pure business logic
  - Zero external dependencies

Application Layer (src/application/):
  - ~300 lines  | 4 use case files
  - DTO definitions
  - Business flow orchestration

Infrastructure Layer (src/infra/):
  - ~1000 lines | 10+ adapter files
  - HTTP routing
  - Database persistence
  - Framework configuration

Total Implementation: ~1900 lines of Python code
Fully functional electronic patient record system

═══════════════════════════════════════════════════════════════════════════════

ENTRY POINTS:

1. Start API Server:
   $ python -m uvicorn src.infra.api.main:app --reload

2. API Documentation:
   http://localhost:8000/docs (Swagger UI)
   http://localhost:8000/redoc (ReDoc)

3. API Root:
   http://localhost:8000/ (status check)

4. Main Endpoints:
   POST   /api/v1/patients/
   GET    /api/v1/patients/{id}
   POST   /api/v1/clinical-records/problems
   POST   /api/v1/clinical-records/soap

5. Health Check:
   http://localhost:8000/health

═══════════════════════════════════════════════════════════════════════════════
"""

print(FILE_TREE)

if __name__ == "__main__":
    print("Run this script to visualize the project structure:")
    print("  $ python src_structure.py")
