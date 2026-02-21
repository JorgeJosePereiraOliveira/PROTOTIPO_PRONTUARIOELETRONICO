<!-- Pronounário Eletrônico - Prototipo -->
# Prontuário Eletrônico - Protótipo em Clean Architecture

Sistema de Prontuário Eletrônico desenvolvido como protótipo, implementando os princípios da **Clean Architecture** conforme definido por Robert C. Martin.

## Visão Geral

Este projeto demonstra a implementação de um Prontuário Eletrônico (Sistema de Registros Clínicos Eletrônicos) organizando o software em camadas concêntricas:

1. **Entidades (Núcleo Clínico)** - RCOP, SOAP, Paciente, Problema Clínico
2. **Casos de Uso (Lógica da Aplicação)** - Registrar SOAP, Criar Problema, Agendar Consulta
3. **Adaptadores (Interface)** - Controllers REST, DTOs, Presenters
4. **Frameworks & Drivers** - FastAPI, SQLAlchemy, Banco de Dados

## Estrutura do Projeto

```
prontuarioeletronico/
├── src/
│   ├── domain/                   # Camada 1: Entidades
│   │   ├── __seedwork/           # Classes base
│   │   ├── patient/              # Paciente
│   │   ├── professional/         # Profissional de Saúde
│   │   ├── clinical_record/      # Registro Clínico (RCOP/SOAP)
│   │   └── appointment/          # Consulta/Agendamento
│   │
│   ├── application/              # Camada 2: Casos de Uso
│   │   ├── patient/              # Registrar paciente
│   │   ├── clinical_record/      # Registrar SOAP, Criar problema
│   │   ├── appointment/          # Agendar consulta
│   │   └── professional/         # regiatrar profissionai
│   │
│   └── infra/                    # Camadas 3 & 4: Adaptadores e Drivers
│       ├── api/                  # Controllers e Routers (FastAPI)
│       ├── patient/              # Repositório Patient
│       ├── clinical_record/      # Repositório Clinical Record
│       └── appointment/          # Repositório Appointment
├── requirements.txt              # Dependências Python
├── Dockerfile                    # Conteinerização
├── docker-compose.yaml           # Orquestração
├── tests.py                      # Suíte de testes unitários
└── README.md                     # Esta documentação
```
# Detalhes da estrutura do projeto:
## Camada 1 (Entidades)
### 1. scr/domain/appontment
O script **appointment_entity.py** define a entidade de domínio Appointment, que representa uma consulta médica no sistema de prontuário eletrônico. Ele encapsula os principais atributos e regras de negócio de uma consulta, incluindo:

- **id**: identificador único da consulta.
- **patient_id**: referência ao paciente.
- **professional_id**: referência ao profissional de saúde.
- **appointment_date**: data e hora da consulta.
- **reason**: motivo da consulta.
- **status**: status da consulta (agendada, concluída, cancelada).
- **notes**: observações adicionais.
- **created_at**: data de criação do registro.
- **updated_at**: data de atualização do registro.

A classe fornece propriedades para acessar esses atributos e métodos para:
- **mark_completed**: Marcar a consulta como concluída.
- **cancel**: Cancelar a consulta.
- **reschedule**: Reagendar a consulta.
- **is_overdue**: Verificar se a consulta está atrasada.

Ela herda de Entity, sugerindo que faz parte de um padrão de entidades do domínio. O objetivo é centralizar as regras e dados de uma consulta médica, facilitando a manutenção e evolução do sistema.

### 2. scr/domain/clinical_record
O script **rcop_soap.py** define as entidades centrais do **Registro Clínico Orientado por Problemas (RCOP)**, estruturando o prontuário clínico segundo o modelo **Subjective, Objective, Assessment, Plan (SOAP)**. Ele implementa as seguintes classes principais:

- **Problem**: Representa um problema clínico do paciente (diagnóstico ou condição médica que requer monitoramento e tratamento) dentro do sistema RCOP. É o eixo central em torno do qual as notas SOAP são organizadas. Apresenta os seguintes atributos:

    - **id**: Identificador único para o problema.
    - **patient_id**: Referência ao paciente.
    - **description**: Descrição clínicqa do problema.
    - **icd10_code**: Código ICD-10 do problema.
    - **status**: Active, resolved, archived (ativo, resolvido ou arquivado).
    - **created_at**: Data e hora de criação.
    - **updated_at**: Data e hora de atualização.
    - **métodos para resolver, arquivar e atualizar a descrição do problema**.

- **Subjective**: Representa a parte “Subjetiva” da nota SOAP, contendo:
    - **id**.
    - **clinical_record_id**.
    - **Queixas do paciente**.
    - **Histórico médico**.
    - **Medicamentos**.
    - **Alergias que o paciente sofre**.
    - **Data de criação**.
- **Objective**: Representa a parte “Objetiva” da nota SOAP, com:
    - **id**.
    - **clinical_record_id**.
    - **Sinais vitais**.
    - **Exame físico**.
    - **Resultados laboratoriais**.
    - **Resultados de imagens**.
    - **Data de criação**.
- **Assessment**: Representa a “Avaliação” (Assessment), incluindo:
    - **id**.
    - **clinical_record_id**.
    - **Diagnóstico**.
    - **Impressão clínica**.
    - **Diagnósticos diferenciais**.
    - **Problemas relacionados**.
    - **Data de criação**.
- **Plan**: Representa o “Plano” de tratamento, com:
    - **id**.
    - **clinical_record_id**.
    - **Plano terapêutico**.
    - **Medicamentos**.
    - **Procedimentos**.
    - **Recomendações de seguimento e procedimentos futuros**.
    - **Data de criação**.

- **ClinicalRecord**: Representa o registro clínico completo de um atendimento, agregando todas as partes do SOAP:
    - **id**.
    - **patient_id**: Informações do paciente.
    - **professional_id**: Informações do profissional.
    - **problem_id**: Problema associado.
    - **encounter_date**: Data do encontro.
    - **subjective**.
    - **objective**.
    - **assessment**.
    - **plan**.
    - **created_at**: Data de criação.
    - **updated_at**: Data de atualização.
    - **Métodos para atualizar cada componente SOAP e verificar se todos os registros SOAP estão completo**.

Portanto, o script **rcop_soap.py** modela toda a estrutura de um prontuário clínico orientado por problemas, permitindo criar, atualizar e consultar cada parte do registro de forma organizada e seguindo padrões médicos reconhecidos. Ele é fundamental para garantir a integridade, rastreabilidade e padronização dos dados clínicos no sistema.
### 3. scr/domain/patient
O script **patient_entity.py** codifica a entidade de domínio paciente. Representa o paciente (pessoa atendida) dentro do sistema. A classe Patient(Entity) representa um paciente no sistema eletrônico de registros de pacientes e encapsula os atributos e regras de negócios seguintes:
  - **id**: Identificador único do paciente.
  - **name**: Nome completo do paciente.
  - **date_of_birth**: Data de nascimento.
  - **gender**: Sexo (M, F, O, N).
  - **cpf**: CPF.
  - **email**: Optional.
  - **phone**: Optional.
  - **address**: Optional para pacientes em situação de rua.
  - **city**: Cidade.
  - **state**: Estado (UF).
  - **insurance**: Informações sobre o seguro de saúde ou plano de saúde.
  - **created_at**: Data/hora de criação do registro.
  - **updated_at**: Data/hora de atualização do registro.
  - **Métodos para calcular a idade do paciente em anos, atualizar informação de contato do paciente (email e telefone), atualizar endereço do paciente (endereço, cidade e UF) e atualizar seguro ou plano de saúde do paciente**.

### 4. scr/domain/profissional
A entidade profissional (**profissional_entity.py**) representa um profissional de saúde no sistema eletrônico. Esta entidade encapsula o código de atributos e as regras de negócio relativo aos profissionais de saúde (médicos, enfermeiros, psicologos, etc.). Os atributos são:
  - **id**: Identificador ínico do profissional.
  - **name**: Nome completo do profissional.
  - **license_number**: Número da licença do profissional.
  - **specialties**: Lista das especialidades do profissional.
  - **crm**: CRM number (Conselho Regional de Medicina).
  - **email**: Email do profissional (Optional).
  - **phone**: Telefone do profissional (Optional).
  - **institution**: Instituição ou clinica atual (Optional).
  - **created_at**: Data/hora de criação do registro (Optional).
  - **updated_at**: Data/hora de atualização do registro (Optional).
  - **Métodos para adicionar uma nova especialidade na ista do especialidades do profissional, remover um especialidade da lista, atualizar a instituição atual do profissional e confirmar se o profissional tem uma especialidade específica**.

## Camada 2 (Casos de uso)
### 1. scr/application/appointment
O script **schedule_appointment_usecase.py** implementa o caso de uso para **Agendar Consulta**. Ele segue o padrão de arquitetura de "Use Case" (caso de uso), separando regras de negócio da infraestrutura. O script implementa as seguites classes:
**DTOs (Data Transfer Objects)**:
- **class ScheduleAppointmentDTO**: Objeto de transferência de dados para agendamento de consulta (recebe dados necessários para agendar uma consulta).
Os atributos desta classe são:
    - **patient_id**: Identificador do paciente.
    - **professional_id**: Identificador do profissional.
    - **appointment_date**: Data/hora da consulta.
    - **reason**: Motivo da consulta.
    - **notes**: Observações adicionais sobre a consulta.

- **class ScheduleAppointmentOutputDTO**: Objeto de transferência de dados para saida de agendamento de consulta. Retorna o resultado do agendamento (id da consulta, mensagem de sucesso).
Os atributos dessa classe são:
    - **appointment_id**: Identificador da consulta.
    - **message**: Mensagem de sucesso (mensagem de saida do agendamento da consulta).

**Classe principal**:
- **class ScheduleAppointmentUseCase(UseCase[ScheduleAppointmentDTO, ScheduleAppointmentOutputDTO])**:  Herda de UseCase (interface genérica do domínio). Recebe um repositório de consultas (appointment_repository) para persistência. Método execute: valida os dados, cria uma entidade Appointment, persiste no repositório e retorna o resultado. Métodos auxiliares: _validate_input (valida regras de negócio) e _generate_id (gera id único). Assim, na sequência:
    - **Use Case para agendar nova consulta**.
    - **Executar o use case da nova consulta**: Validate input; Create appointment entity; Persist the appointment.
    - **Valida entrada (imput) de acordo com as regras de negócio**.
    - **Gera um ID único**.

Os atributos dessa classe são:
- **appointment_repository**.

Relação com outros scripts
- **Importações**:
    - Usa a interface **UseCase** de **use_case_interface.py**, garantindo padronização dos casos de uso.
    - Usa a entidade **Appointment** de **appointment_entity.py**, representando a consulta.
    - O repositório passado ao construtor deve implementar a interface de repositório de consultas, provavelmente definida em **appointment_repository_interface.py**.
- **Fluxo de dados**:
    - O caso de uso é chamado por camadas superiores (ex: API, interface gráfica), recebe dados via DTO, valida, cria a entidade, persiste e retorna o resultado.
    - O repositório pode ser implementado na camada de infraestrutura, por exemplo, usando SQLAlchemy (**infra/appointment/sqlalchemy/**).
- **Integração**:
    - O script é parte da camada de aplicação, conectando domínio (entidades, regras) e infraestrutura (persistência).
    - Pode ser utilizado por roteadores de API (**infra/api/routers/**) para expor endpoints de agendamento.

### 2. scr/application/clinical_record
### **2.1. scr/application/clinical_record/create_problem_usecase.py**
Este script implementa um Use Case para Criar/Regiatrar um novo ploblema clínico, na seguinte sequência:
- **class CreateProblemDTO**: Objeto de transferência de dados (DTO) para criar um novo problema clínico.
- **class CreateProblemOutputDTO**: Objeto de transferência de dados para criar uma saída (um output de mensagem) do novo problema clínico criado.
- **class CreateProblemUseCase(UseCase[CreateProblemDTO, CreateProblemOutputDTO])**: Use Case para criar um novo problema clínico no sistema RCOP. Este caso de uso lida com o registro de um novo problema de saúde que será gastreado e monitorado por meio de notas SOAP. Essa classe executa o use case para criar um novo problema clínico do seguinte modo: Argumentos: **input_dto**: Entrada de daods para um novo problema; Retornos: **CreateProblemOutputDTO**: Resultado com o ID do novo problema clínico criado. Logo, os argumentos dessa classe **valida imput_dto**, **cria a entidade problema** (gera id, patient_id, description, icd10_code, status), **perciste o novo  problema clínico criado** e retorna a mensagem **problema clínico criao com sucesso**. Por fim, a classe valida o imput de acordo com as regras de negócio e garante um ID único.
### **2.2. scr/application/clinical_record/register_soap_usecase.py**
Este script implementa um Use Case para registrar uma nova nota clínica SOAP. Cria um registro clínico completo seguindo a estrutura SOAP, de acordo com a seguinte estrutura:
- **class RegisterSOAPDTO**: Implementa o objeto de transferência de dados (DTO) para registrar uma nota SOAP, com os seguintes argumentos:
    - **patient_id**.
    - **professional_id**.
    - **problem_id**.
    - **encounter_date**: Data/hora da consulta.
    - **patient_complaint**.
    - **vital_signs**: Sinais vitais.
    - **physical_examination**.
    - **diagnosis**.
    - **treatment_plan**.
    - **medical_history**: Histórico médico (Optional),
    - **lab_results**.
    - **medications**.
    - **allergies**.
    - **clinical_impression**.
- **class RegisterSOAPOutputDTO**: Implementa objeto de transferência de dados para saída (autput) de registro de SOAP.
- **class RegisterSOAPUseCase(UseCase[RegisterSOAPDTO, RegisterSOAPOutputDTO])**: Caso de uso para registrar uma nova nota clínica SOAP. Esse Use Case orquestra a criação de um registro clínico completo com todos os compontentes SOAP (Subjective, Objective, Assessment, Plan), valida imput DTO, cria componentes SOAP (***Subjective*: id; clinical_record_id, que será atualizado quando o registro for criado; patient_complaint; medical_history; medications; allergies - *Objective*: id; clinical_record_id; vital_signs; physical_examination; lab_results - *Assessment*: id; clinical_record_id; diagnosis; clinical_impression; related_problems - *Plan*: id; clinical_record_id; treatment_plan; medications**), cria o registro clínico (**id; patient_id; professional_id; problem_id; encounter_date; subjective; objective; assessment; plan**), perciste o registro (retorna a mensagem 'SOAP clinical record registered successfully'), valida entrada de dados de acordo com as regras de negócio, gerar um ID único. Essa classe implementa:
- **Executa o use case para registro da nota SOAP**.
- **Argumento input_dto**: Entrada de dados (Input data) contendo todos os componentes SOAP.
- **Retono: RegisterSOAPOutputDTO**. Resulta com o ID do registro clínico criado.
- **Exceção**: Se a validação ou operação do repositório falharem.

### 3. scr/application/patient
O script **register_patient_usecase**


## Princípios de Clean Architecture Aplicados ao projeto

### 1. Regra da Dependência
- Dependências sempre apontam para dentro
- Camadas internas nunca conhecem camadas externas
- As regras clínicas (RCOP/SOAP) no núcleo são independentes de tecnologia

### 2. Isolamento de Responsabilidades
- **Domain**: Regras de negócio corporativas (SOAP, RCOP, paciente)
- **Application**: Orquestração de casos de uso
- **Infrastructure**: Detalhes técnicos (banco de dados, APIs)

### 3. Testabilidade
- Lógica clínica pode ser testada sem banco de dados ou UI
- Repositórios são interfaces, implementações são injetáveis
- Use cases não conhecem frameworks

### Realização de testes do projeto durante o desenvolvimento:
O comando **python -m prontuarioeletronico.tests** roda todos os testes definidos no arquivo **tests.py** do projeto, com os seguintes detalhes:
O arquivo **tests.py** contém uma suíte de testes unitários, escritos usando o framework unittest do Python.
Cada classe de teste (por exemplo, TestAppointment, TestPatientEntity) testa uma parte específica do domínio do sistema, como entidades de paciente, consulta, prontuário clínico, etc.
Dentro dessas classes, métodos que começam com **test_** verificam funcionalidades específicas, como criação de objetos, métodos de negócio (ex: marcar consulta como concluída, cancelar, reagendar), validação de atributos, entre outros.
Ao rodar **python -m prontuarioeletronico.tests**, o Python executa todos os métodos de teste definidos nesse arquivo.
O resultado OK significa que todas as funcionalidades testadas estão funcionando conforme esperado, sem erros ou falhas.
Portanto, o script **tests.py** é o ponto central de validação automática do projeto. Ele garante que as entidades e regras de negócio implementadas nos outros scripts (como appointment_entity.py) estão corretas e continuam funcionando após alterações no código.
Logo, sempre que modificar ou adicionar funcionalidades ao sistema, pode (e deve) rodar esse teste para garantir que nada foi quebrado, validando automaticamente o comportamento das principais entidades e regras do seu projeto.


### 4. Independência Tecnológica
- Trocar banco de dados não afeta regras de negócio
- Trocar framework não afeta casos de uso
- SOAP/RCOP permanece intacto em mudanças tecnológicas

## Implementação RCOP/SOAP

O protótipo implementa o padrão clínico **Problem-Oriented Clinical Record (RCOP)** com estrutura **SOAP**:

### Estrutura SOAP:
- **S (Subjective)**: Queixa do paciente e história
- **O (Objective)**: Achados do exame físico e testes
- **A (Assessment)**: Diagnóstico e avaliação clínica
- **P (Plan)**: Plano de tratamento e seguimento

### Fluxo de Registro:
1. Registrar Problema Clínico → Cria um eixo de documentação
2. Registrar Encontro SOAP → Documentação estruturada por problema
3. Evolução Clínica → Novos SOAP notes para mesmo problema

## Casos de Uso Implementados

1. **RegisterPatientUseCase** - Registrar novo paciente
2. **CreateProblemUseCase** - Criar problema clínico (RCOP)
3. **RegisterSOAPUseCase** - Registrar encontro clínico com SOAP
4. **ScheduleAppointmentUseCase** - Agendar consulta

## Como Executar

### Opção 1: Local com Python

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python -m uvicorn src.infra.api.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse: http://localhost:8000/docs (Swagger UI)

### Opção 2: Docker

```bash
# Build e executar
docker-compose up --build

# API será acessível em http://localhost:8000
```

## Exemplos de Uso

### 1. Registrar Paciente

```bash
curl -X POST http://localhost:8000/api/v1/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "date_of_birth": "1990-05-15T00:00:00",
    "gender": "M",
    "cpf": "12345678901",
    "email": "joao@example.com",
    "phone": "11999999999",
    "address": "Rua A, 123",
    "city": "São Paulo",
    "state": "SP",
    "insurance": "Unimed"
  }'
```

### 2. Criar Problema Clínico

```bash
curl -X POST http://localhost:8000/api/v1/clinical-records/problems \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient-123",
    "description": "Hipertensão arterial sistêmica",
    "icd10_code": "I10"
  }'
```

### 3. Registrar SOAP

```bash
curl -X POST http://localhost:8000/api/v1/clinical-records/soap \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient-123",
    "professional_id": "prof-456",
    "problem_id": "problem-789",
    "encounter_date": "2024-02-13T10:30:00",
    "patient_complaint": "Pressão elevada",
    "vital_signs": "PA: 150/95, FC: 72, FR: 16",
    "physical_examination": "Sem alterações",
    "diagnosis": "Hipertensão não controlada",
    "treatment_plan": "Ajuste de medicação"
  }'
```

## Arquitetura em Diagrama

```
┌─────────────────────────────────────────────────────────────┐
│ CAMADA 4: FRAMEWORKS & DRIVERS (Detalhes Externos)          │
│ - FastAPI, SQLAlchemy                                       │
│ - SQLite/PostgreSQL                                         │
│ - Docker, Kubernetes                                        │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│ CAMADA 3: ADAPTADORES (Interface)                           │
│ - Controllers REST                                          │
│ - DTOs (Presenters)                                         │
│ - Repositórios (Implementações SQLAlchemy)                  │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│ CAMADA 2: CASOS DE USO (Lógica da Aplicação)               │
│ - RegisterPatient                                           │
│ - RegisterSOAP                                              │
│ - CreateProblem                                             │
│ - ScheduleAppointment                                       │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│ CAMADA 1: ENTIDADES (Regras de Negócio)                    │
│ - Patient (Paciente)                                        │
│ - Problem (Problema - RCOP)                                 │
│ - ClinicalRecord (Registro - SOAP)                          │
│ - Appointment (Consulta)                                    │
└─────────────────────────────────────────────────────────────┘
```

## Tabelas de Banco de Dados

| Tabela | Descrição |
|--------|-----------|
| patients | Pacientes |
| professionals | Profissionais de saúde |
| problems | Problemas clínicos (RCOP) |
| clinical_records | Registros clínicos |
| soap_subjectives | Componente S do SOAP |
| soap_objectives | Componente O do SOAP |
| soap_assessments | Componente A do SOAP |
| soap_plans | Componente P do SOAP |
| appointments | Agendamentos |

## Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados (DTOs)
- **SQLite** - Banco de dados (desenvolvimento)
- **Uvicorn** - Servidor ASGI
- **Docker** - Conteinerização
- **Docker Compose** - Orquestração local

## Próximas Etapas

1. Adicionar autenticação e autorização
2. Implementar mais casos de uso (buscar, atualizar, deletar)
3. Adicionar testes unitários e de integração
4. Implementar pipeline CI/CD
5. Integração com IA Service para sugestões diagnósticas
6. Auditoria de eventos clínicos
7. Segurança LGPD (criptografia de dados sensíveis)

## Referências

- Martin, R. C. (2008). "The Clean Architecture". Robert C. Martin
- Martin, R. C. (2017). "Clean Architecture: A Craftsman's Guide to Software Structure and Design"
- TCC: Arquitetura e Implementação de Prontuário Eletrônico em Clean Architecture

## Autor

Jorge Oliveira

---

**Status**: Protótipo em desenvolvimento  
**Última atualização**: Fevereiro de 2024
