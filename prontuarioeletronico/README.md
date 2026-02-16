<!-- Pronounário Eletrônico - Prototipo -->
# Prontuário Eletrônico - Protótipo em Clean Architecture

Sistema de Prontuário Eletrônico desenvolvido como protótipo para TCC, implementando os princípios da **Clean Architecture** conforme definido por Robert C. Martin.

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
│   ├── domain/                    # Camada 1: Entidades
│   │   ├── __seedwork/           # Classes base
│   │   ├── patient/              # Paciente
│   │   ├── professional/         # Profissional de Saúde
│   │   ├── clinical_record/      # Registro Clínico (RCOP/SOAP)
│   │   └── appointment/          # Consulta/Agendamento
│   │
│   ├── application/              # Camada 2: Casos de Uso
│   │   ├── patient/              # Registrar paciente
│   │   ├── clinical_record/      # Registrar SOAP, Criar problema
│   │   └── appointment/          # Agendar consulta
│   │
│   └── infra/                    # Camadas 3 & 4: Adaptadores e Drivers
│       ├── api/                  # Controllers e Routers (FastAPI)
│       ├── patient/              # Repositório Patient
│       ├── clinical_record/      # Repositório Clinical Record
│       └── appointment/          # Repositório Appointment
├── requirements.txt              # Dependências Python
├── Dockerfile                    # Conteinerização
├── docker-compose.yaml           # Orquestração
└── README.md                     # Esta documentação
```

## Princípios de Clean Architecture Aplicados

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

Desenvolvimento como parte do Trabalho de Conclusão de Curso (TCC) em Engenharia de Software.

---

**Status**: Protótipo em desenvolvimento  
**Última atualização**: Fevereiro de 2024
