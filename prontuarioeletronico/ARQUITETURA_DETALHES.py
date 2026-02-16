"""
ARQUITETURA DO SISTEMA - Detalhes Técnicos

Este arquivo documenta como a Clean Architecture foi implementada
no protótipo do Prontuário Eletrônico.
"""

# ============================================================================
# CAMADA 1: ENTIDADES (Domain Layer) - Núcleo Clínico Isolado
# ============================================================================

"""
Localização: src/domain/

Características:
- Nenhuma dependência externa
- Sem imports de FastAPI, SQLAlchemy ou frameworks
- Contém apenas lógica corporativa vital
- Completamente testável sem infra

Entidades principais:

1. PATIENT (src/domain/patient/patient_entity.py)
   - Encapsula dados e regras de um paciente
   - Métodos: calculate_age(), update_contact_info(), update_address()
   - Responsabilidade: Dados e validações do paciente

2. PROFESSIONAL (src/domain/professional/professional_entity.py)
   - Profissional de saúde
   - Métodos: add_specialty(), remove_specialty(), has_specialty()
   - Responsabilidade: Dados do profissional

3. PROBLEM (src/domain/clinical_record/rcop_soap.py)
   - Problema clínico (eixo RCOP)
   - Métodos: resolve_problem(), archive_problem(), update_description()
   - Responsabilidade: Gerenciar problemas clínicos e status

4. CLINICAL RECORD COMPONENTS (Subjective, Objective, Assessment, Plan)
   - Componentes SOAP
   - Cada um é uma entidade separada
   - Responsabilidade: Estruturar documentação clínica

5. CLINICAL_RECORD
   - Agrega os componentes SOAP
   - Métodos: set_subjective(), set_objective(), is_complete()
   - Responsabilidade: Orquestração dos componentes SOAP

6. APPOINTMENT
   - Consulta/Agendamento
   - Métodos: mark_completed(), cancel(), reschedule(), is_overdue()
   - Responsabilidade: Gerenciar ciclo de vida da consulta

Base Classes (src/domain/__seedwork/):
- Entity: Base para todas as entidades
- UseCase: Interface para todos os casos de uso
- RepositoryInterface: Contrato para repositórios

Regra de Dependência:
✓ Domain Layer não depende de nada externo
✓ Application Layer depende de Domain
✓ Infrastructure Layer depende de Domain e Application
✓ Nunca o inverso!
"""

# ============================================================================
# CAMADA 2: CASOS DE USO (Application Layer) - Orquestração
# ============================================================================

"""
Localização: src/application/

Características:
- Orquestra fluxo de dados entre entidades
- Independente de frameworks
- Implementa regras específicas da aplicação
- Usa repositórios via injeção de dependência

Casos de Uso implementados:

1. RegisterPatientUseCase (src/application/patient/register_patient_usecase.py)
   Entrada: RegisterPatientDTO
   - name, date_of_birth, gender, cpf, email, phone, address, etc.
   Saída: RegisterPatientOutputDTO
   - patient_id, message
   Fluxo:
   1. Validar entrada
   2. Criar entidade Patient
   3. Persistir via repository.add()
   4. Retornar resultado

2. CreateProblemUseCase (src/application/clinical_record/create_problem_usecase.py)
   Entrada: CreateProblemDTO
   - patient_id, description, icd10_code
   Saída: CreateProblemOutputDTO
   - problem_id, message
   Fluxo:
   1. Validar entrada
   2. Criar entidade Problem
   3. Persistir via repository.add()
   4. Retornar resultado

3. RegisterSOAPUseCase (src/application/clinical_record/register_soap_usecase.py)
   Entrada: RegisterSOAPDTO
   - patient_id, professional_id, problem_id, encounter_date, S/O/A/P data
   Saída: RegisterSOAPOutputDTO
   - clinical_record_id, message
   Fluxo:
   1. Validar entrada (regras de negócio)
   2. Criar componentes SOAP (Subjective, Objective, Assessment, Plan)
   3. Criar entidade ClinicalRecord agregando componentes
   4. Persistir via repository.add()
   5. Retornar resultado

4. ScheduleAppointmentUseCase (src/application/appointment/schedule_appointment_usecase.py)
   Entrada: ScheduleAppointmentDTO
   - patient_id, professional_id, appointment_date, reason
   Saída: ScheduleAppointmentOutputDTO
   - appointment_id, message
   Fluxo:
   1. Validar entrada (data no futuro, etc.)
   2. Criar entidade Appointment
   3. Persistir via repository.add()
   4. Retornar resultado

DTOs (Data Transfer Objects):
- InputDTO: Transportam dados da HTTP request para o use case
- OutputDTO: Transportam resultado do use case para HTTP response
- Função: Desacoplar controller da lógica interna

Padrão de Implementação:
```python
class MyUseCase(UseCase[InputDTO, OutputDTO]):
    def __init__(self, repository):
        self._repository = repository
    
    def execute(self, input_dto: InputDTO) -> OutputDTO:
        # 1. Validar
        self._validate_input(input_dto)
        # 2. Criar entidades
        entity = MyEntity(...)
        # 3. Persistir
        self._repository.add(entity)
        # 4. Retornar resultado
        return OutputDTO(...)
```

Injeção de Dependência:
- Repositório é injetado no construtor
- Permite substituir implementação real por mock nos testes
- Desacopla lógica de persistência
"""

# ============================================================================
# CAMADA 3: ADAPTADORES (Interface Adapters Layer) - Conversão
# ============================================================================

"""
Localização: src/infra/api/

Características:
- Converte HTTP ↔ Caso de Uso ↔ Banco de Dados
- Controllers (Routers)
- DTOs de API (Pydantic)
- Presenters

Controllers/Routers:

1. patient_routers.py (src/infra/api/routers/patient_routers.py)
   - POST /api/v1/patients/ → create_patient()
     * Recebe PatientCreateRequest (HTTP JSON)
     * Cria RegisterPatientDTO
     * Chama RegisterPatientUseCase
     * Retorna dict com resultado
   
   - GET /api/v1/patients/{patient_id} → get_patient()
     * Chama repository.find_by_id()
     * Formata resposta
   
   - GET /api/v1/patients/ → list_patients()
     * Chama repository.find_all()
     * Retorna lista formatada

2. clinical_record_routers.py
   - POST /api/v1/clinical-records/soap → register_soap_note()
   - POST /api/v1/clinical-records/problems → create_problem()

Presenters (DTOs de API):

src/infra/api/presenters/patient_presenter.py:
- PatientCreateRequest: Pydantic model para entrada
- PatientResponse: Pydantic model para saída

src/infra/api/presenters/clinical_record_presenter.py:
- RegisterSOAPRequest
- CreateProblemRequest
- ClinicalRecordResponse

Função:
- Validação automática de entrada
- Documentação automática no Swagger
- Conversão JSON ↔ Python
- Isolamento de mudanças de API

Fluxo HTTP → Use Case → Domain:

Request HTTP JSON
    ↓
Presenter (Pydantic) - Valida e deserializa
    ↓
Router (Controller) - Recebe dados validados
    ↓
Cria InputDTO
    ↓
UseCase.execute(input_dto)
    ↓
Domain Entities - Lógica pura
    ↓
Repository.add() / update()
    ↓
OutputDTO
    ↓
Router - Formata resposta
    ↓
Response HTTP JSON
"""

# ============================================================================
# CAMADA 4: FRAMEWORKS & DRIVERS (External Details) - Implementação
# ============================================================================

"""
Localização: src/infra/

Características:
- Detalhes de implementação
- Pode mudar sem afetar camadas internas
- SQLAlchemy, FastAPI, Banco de Dados

Banco de Dados:

src/infra/api/database.py:
- SQLite para desenvolvimento
- Pode ser trocado por PostgreSQL em produção
- SessionLocal factory
- get_db() para dependency injection

Modelos SQLAlchemy (Entidades não são modelos ORM):

src/infra/patient/sqlalchemy/patient_model.py:
- PatientModel: Mapeamento relacional do Patient
- Tabela: patients
- Colunas: id, name, date_of_birth, gender, cpf, etc.
- NOT linked directly to domain Entity

src/infra/clinical_record/sqlalchemy/clinical_record_model.py:
- ClinicalRecordModel
- ProblemModel
- SubjectiveModel, ObjectiveModel, AssessmentModel, PlanModel
- Tabelas normalizadas para SOAP

src/infra/appointment/sqlalchemy/appointment_model.py:
- AppointmentModel

Repositórios (Implementação concreta):

src/infra/patient/sqlalchemy/patient_repository.py:
```python
class PatientRepository(RepositoryInterface[Patient]):
    def add(self, entity: Patient) -> None:
        model = PatientModel(id=entity.id, name=entity.name, ...)
        self._db.add(model)
        self._db.commit()
    
    def find_by_id(self, id: str) -> Optional[Patient]:
        model = self._db.query(PatientModel).filter(...).first()
        return self._to_domain(model)
    
    def _to_domain(self, model: PatientModel) -> Patient:
        return Patient(id=model.id, name=model.name, ...)
```

Função:
- Converte entre ORM Model ↔ Domain Entity
- Implementa RepositoryInterface
- Não é conhecido pela aplicação

Configuração FastAPI:

src/infra/api/config.py:
- create_app(): Retorna app FastAPI configurado
- CORS middleware
- Error handlers

src/infra/api/main.py:
- Importa routers
- app.include_router(patient_routers.router)
- app.include_router(clinical_record_routers.router)
- Endpoints raiz (/health, /api/v1, etc.)
"""

# ============================================================================
# FLUXO COMPLETO DE UMA REQUISIÇÃO
# ============================================================================

"""
Exemplo: Registrar um novo paciente

1. HTTP POST /api/v1/patients/
   {
     "name": "João Silva",
     "date_of_birth": "1990-05-15T00:00:00",
     "gender": "M",
     "cpf": "12345678901",
     ...
   }

2. FastAPI Router (patient_routers.py::create_patient)
   - Recebe PatientCreateRequest validado por Pydantic
   - Cria instância de PatientRepository(db)
   - Cria instância de RegisterPatientUseCase(repository)

3. RegisterPatientUseCase.execute()
   - Valida RegisterPatientDTO:
     * name não vazio
     * cpf válido (11+ dígitos)
     * gender em [M, F, O, N]
   - Cria entidade Patient (núcleo puro, sem DB)
   - Chama repository.add(patient)

4. PatientRepository.add(Patient entity)
   - Converte Patient → PatientModel (ORM)
   - Executa SQL INSERT
   - Commit na transaction
   - Retorna sucesso

5. Use Case retorna RegisterPatientOutputDTO
   - patient_id: ID gerado
   - message: "Paciente João Silva registrado com sucesso"

6. Router formata resposta HTTP
   {
     "patient_id": "uuid-12345",
     "message": "Patient João Silva registered successfully"
   }

7. FastAPI serializa para JSON e retorna HTTP 200 OK

Separação de Responsabilidades:
- HTTP: FastAPI Router (não conhece lógica de negócio)
- Lógica: UseCase (não conhece HTTP nem DB)
- Dados: Entity (não conhece persistência)
- Persistência: Repository (não conhece casos de uso)
"""

# ============================================================================
# COMO A ARQUITETURA FACILITA MANUTENÇÃO DO RCOP/SOAP
# ============================================================================

"""
Cenário 1: Ministério da Saúde adiciona novo campo em SOAP
Mudança necessária: Adicionar campo "Prescrição" em Plan

Único lugar a mudar:
1. src/domain/clinical_record/rcop_soap.py::Plan
   - Adicionar propriedade _prescription
   - Adicionar property prescription

2. src/application/clinical_record/register_soap_usecase.py
   - Atualizar RegisterSOAPDTO
   - Passar prescription para Plan()

3. src/infra/clinical_record/sqlalchemy/clinical_record_model.py
   - Adicionar coluna prescription em PlanModel

4. src/infra/api/presenters/clinical_record_presenter.py
   - Adicionar field prescription no RegisterSOAPRequest

HTTP, Controllers, Repositórios genéricos não mudam!
A regra clínica está protegida no centro.

Cenário 2: Trocar banco de dados SQL por MongoDB

Arquivos a mudar:
- src/infra/clinical_record/sqlalchemy/clinical_record_repository.py
  Criar novo: src/infra/clinical_record/mongodb/clinical_record_repository.py

Domain, Application, API Routers NÃO MUDAM!
Repositório é interface, implementação é detalhe.

Cenário 3: Adicionar validação clínica "Assessment deve referenciar Problem"

Único lugar:
- src/domain/clinical_record/rcop_soap.py::Assessment.__init__()
  Validar que related_problems não está vazio

Ou em:
- src/application/clinical_record/register_soap_usecase.py::_validate_input()

Toda aplicação garante validade automaticamente!

Benefício: RCOP/SOAP é protegido de mudanças tecnológicas
"""

# ============================================================================
# TESTABILIDADE DA ARQUITETURA
# ============================================================================

"""
Teste Unitário de Domain:
```python
def test_patient_calculate_age():
    patient = Patient(
        id="p1",
        name="João",
        date_of_birth=datetime(1990, 5, 15),
        gender="M",
        cpf="123"
    )
    age = patient.calculate_age()
    assert age == 34  # 2024 - 1990
```
✓ Sem banco de dados
✓ Sem HTTP
✓ Sem frameworks
✓ Executa em millisegundos

Teste Unitário de Use Case:
```python
def test_register_patient_usecase(mock_repository):
    use_case = RegisterPatientUseCase(mock_repository)
    input_dto = RegisterPatientDTO(...)
    output = use_case.execute(input_dto)
    assert output.patient_id is not None
    mock_repository.add.assert_called_once()
```
✓ Mock repository
✓ Sem banco de dados
✓ Sem HTTP
✓ Testa lógica pura

Teste de Integração:
```python
def test_api_create_patient(client, db_session):
    response = client.post("/api/v1/patients/", json={...})
    assert response.status_code == 200
    assert response.json()["patient_id"] is not None
    # Verifica se foi realmente persistido
    patient = db_session.query(PatientModel).first()
    assert patient.name == "João"
```
✓ Testa HTTP ↔ Use Case ↔ Database

Pipeline CI/CD:
1. Testes Unitários (rápido, sem dependências)
2. Testes de Integração (com DB em memória)
3. Build Docker
4. Deploy
"""

# ============================================================================
# RESUMO: COMO A ARQUITETURA LIMPA PROTEGE O PRONTUÁRIO
# ============================================================================

"""
1. Isolamento de Regras Clínicas
   - RCOP/SOAP no center, puro e testável
   - Independente de tecnologia
   - Fácil de manter e evoluir

2. Separação de Responsabilidades
   - Cada camada tem um papel claro
   - Mudanças localizadas
   - Reutilização de código

3. Testabilidade
   - Regras clínicas sem DB ou UI
   - Casos de uso com mock
   - Integração com cliente real

4. Independência Tecnológica
   - Banco de dados é detalhe
   - Framework web é detalhe
   - Regras clínicas são o core

5. Escalabilidade
   - Fácil adicionar novos casos de uso
   - Microsserviços possível
   - Sem quebra de compatibilidade

Conclusão:
Clean Architecture garante que o Prontuário Eletrônico pode evoluir
por 20+ anos, mesmo com mudanças tecnológicas constantes, mantendo
a integridade das regras clínicas (RCOP/SOAP) intact.
"""
