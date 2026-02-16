# GUIA RÁPIDO - Prontuário Eletrônico em Clean Architecture

## 📁 Estrutura em Uma Linha

```
domain/ (entidades) → application/ (casos de uso) → infra/api/ (HTTP) + infra/*/repo/ (DB)
```

## 🎯 4 Camadas

| Camada | Localização | Função | Dependências |
|--------|------------|--------|--------------|
| **1. Entidades** | `src/domain/` | Regras RCOP/SOAP | Nenhuma |
| **2. Casos de Uso** | `src/application/` | Orquestração | Domain |
| **3. Adaptadores** | `src/infra/api/` | HTTP ↔ Use Case | App + Domain |
| **4. Drivers** | `src/infra/*.repo/` | Persistência | Todos |

## 📚 Entidades Principais

| Entidade | Arquivo | Responsabilidade |
|----------|---------|------------------|
| `Patient` | `domain/patient/patient_entity.py` | Dados do paciente |
| `Professional` | `domain/professional/professional_entity.py` | Dados profissional |
| `Problem` | `domain/clinical_record/rcop_soap.py` | Problema RCOP |
| `ClinicalRecord` | `domain/clinical_record/rcop_soap.py` | Registro (SOAP) |
| `Subjective, Objective, Assessment, Plan` | `domain/clinical_record/rcop_soap.py` | Componentes SOAP |
| `Appointment` | `domain/appointment/appointment_entity.py` | Agendamento |

## 🔄 Fluxo: Patient Registration

```
POST /api/v1/patients/ 
    ↓ JSON Request
PatientCreateRequest (Pydantic validation)
    ↓
patient_routers.py::create_patient()
    ↓
RegisterPatientUseCase.execute(InputDTO)
    ↓
Patient Entity (domain logic)
    ↓
PatientRepository.add(patient)
    ↓
PatientModel (SQLAlchemy)
    ↓
Database INSERT
    ↓
OutputDTO → JSON Response
```

## 🚀 Quick Start

### Windows
```batch
cd prontuarioeletronico
quickstart.bat
```

### Linux/Mac
```bash
cd prontuarioeletronico
bash quickstart.sh
```

### Docker
```bash
docker-compose up --build
curl http://localhost:8000/docs
```

## 📡 Principais Endpoints

| Método | Endpoint | Função |
|--------|----------|--------|
| `POST` | `/api/v1/patients/` | Registrar paciente |
| `GET` | `/api/v1/patients/{id}` | Buscar paciente |
| `GET` | `/api/v1/patients/` | Listar pacientes |
| `POST` | `/api/v1/clinical-records/problems` | Criar problema (RCOP) |
| `POST` | `/api/v1/clinical-records/soap` | Registrar SOAP |

## 🧪 Testes

```bash
# Testes unitários (sem DB, sem HTTP)
python -m pytest tests.py -v

# Cobertura
python -m pytest tests.py --cov=src
```

## 🏗️ Casos de Uso Implementados

| Caso de Uso | Arquivo | Entrada | Saída |
|------------|---------|---------|-------|
| Registrar Paciente | `application/patient/register_patient_usecase.py` | PatientDTO | patient_id |
| Criar Problema | `application/clinical_record/create_problem_usecase.py` | ProblemDTO | problem_id |
| Registrar SOAP | `application/clinical_record/register_soap_usecase.py` | SOAPDTO | record_id |
| Agendar Consulta | `application/appointment/schedule_appointment_usecase.py` | AppointmentDTO | appointment_id |

## 📊 Arquitetura Visual

```
                    ┌────────────────────────┐
                    │   HTTP Requests/Responses
                    └────────────┬───────────┘
                                  ↓
    ╔════════════════════════════════════════════════════════════╗
    ║ CAMADA 3: ADAPTADORES (Controllers, DTOs)                  ║
    ║ src/infra/api/routers/ + src/infra/api/presenters/        ║
    ╚════════════════════════════════════════════════════════════╝
                                  ↓
    ╔════════════════════════════════════════════════════════════╗
    ║ CAMADA 2: CASOS DE USO (Orquestração)                      ║
    ║ src/application/*/      *_usecase.py                        ║
    ╚════════════════════════════════════════════════════════════╝
                                  ↓
    ╔════════════════════════════════════════════════════════════╗
    ║ CAMADA 1: ENTIDADES (Núcleo - RCOP/SOAP)                   ║
    ║ src/domain/*/           *_entity.py                         ║
    ╚════════════════════════════════════════════════════════════╝
                                  ↓
    ╔════════════════════════════════════════════════════════════╗
    ║ CAMADA 4: DRIVERS (SQLAlchemy, Banco de Dados)             ║
    ║ src/infra/*/sqlalchemy/ (*_model.py, *_repository.py)      ║
    ╚════════════════════════════════════════════════════════════╝
                                  ↓
                    ┌────────────────────────┐
                    │   Database (SQLite)
                    └────────────────────────┘
```

## ⚙️ Tecnologias

- **Language**: Python 3.10+
- **Web Framework**: FastAPI
- **Server**: Uvicorn  
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Validation**: Pydantic
- **Testing**: unittest/pytest
- **Container**: Docker + Docker Compose

## 🔒 Regra da Dependência

```
✓ CORRETO:
  Infrastructure imports Application
  Application imports Domain
  Domain import nothing (pure business logic)

✗ NUNCA:
  Domain imports Application/Infrastructure
  Application imports Infrastructure (except interfaces)

Resultado: RCOP/SOAP protegido, testável, independente de tecnologia
```

## 📝 Exemplo: Registrar SOAP

### Request
```bash
curl -X POST http://localhost:8000/api/v1/clinical-records/soap \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient-123",
    "professional_id": "prof-456", 
    "problem_id": "problem-789",
    "encounter_date": "2024-02-13T14:30:00",
    "patient_complaint": "Pressão elevada",
    "vital_signs": "PA: 150/95",
    "physical_examination": "Sem alterações",
    "diagnosis": "Hipertensão não controlada",
    "treatment_plan": "Ajustar medicação"
  }'
```

### Response
```json
{
  "clinical_record_id": "uuid-xxxx",
  "message": "SOAP clinical record registered successfully"
}
```

## 🎓 Conceitos Clean Architecture

| Conceito | Implementação |
|----------|---------------|
| **Entidade** | Classes em `domain/` com regras de negócio corporativas |
| **Caso de Uso** | Classes em `application/` que herdam de `UseCase` |
| **Repositório** | Interface em `domain/`, implementação em `infra/` |
| **DTO** | Pydantic models em `infra/api/presenters/` |
| **Injeção de Dependência** | Constructor injection nos Use Cases |
| **Inversão de Dependência** | Repository interface em domain, implementação em infra |

## 🔍 Investigar Código

### Ver uma entidade
```bash
cat src/domain/patient/patient_entity.py
```

### Ver um caso de uso
```bash
cat src/application/patient/register_patient_usecase.py
```

### Ver um router
```bash
cat src/infra/api/routers/patient_routers.py
```

### Ver um repositório
```bash
cat src/infra/patient/sqlalchemy/patient_repository.py
```

## 📖 Documentação Completa

- `README.md` - Overview e instruções
- `ESTRUTURA_PROJETO.py` - Estrutura de pastas detalhada
- `ARQUITETURA_DETALHES.py` - Análise técnica profunda
- `EXEMPLOS_USO.sh` - Exemplos de requisições
- Este arquivo - Referência rápida

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
python -m uvicorn src.infra.api.main:app --port 8001
```

### "Database locked"
```bash
# Remove old database
rm prontuario.db
# Restart
python -m uvicorn src.infra.api.main:app --reload
```

## ✅ Checklist: Implementação Clean Architecture

- [x] Domain layer sem dependências externas
- [x] Application layer com use cases desacoplados
- [x] Interface adapters (HTTP) conversível
- [x] Framework/Drivers isolado (SQLAlchemy)
- [x] Repositório como interface e implementação
- [x] Injeção de dependência
- [x] Testes unitários sem DB/HTTP
- [x] DTOs para transferência de dados
- [x] Documentação completa
- [x] Docker para deploy

## 🎉 Próximas Features

1. Autenticação JWT
2. Auditoria de eventos
3. Integração IA
4. Pesquisa Elasticsearch
5. Cache Redis
6. LGPD compliance
7. API versioning
8. Documentação OpenAPI expandida

---

**Status**: Protótipo funcional | Clean Architecture ✓ | RCOP/SOAP ✓

