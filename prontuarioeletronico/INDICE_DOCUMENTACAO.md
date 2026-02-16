# 📚 ÍNDICE DE DOCUMENTAÇÃO
# Prontuário Eletrônico em Clean Architecture

## 🎯 Comece por aqui

### Para Iniciantes
1. **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** - Referência rápida (5 min)
   - Estrutura em uma linha
   - 4 camadas
   - Endpoints principais
   - Quick start

2. **[README.md](README.md)** - Overview completo (15 min)
   - Versão geral
   - Princípios de Clean Architecture
   - Como executar
   - Exemplos de uso

### Para Compreender a Arquitetura
3. **[ARQUITETURA_VISUAL.py](ARQUITETURA_VISUAL.py)** - Diagrama ASCII (10 min)
   - Anéis concêntricos
   - Fluxo de requisição
   - Matriz de responsabilidades
   - Proteção do RCOP/SOAP

4. **[ARKUITETURA_DETALHES.py](ARQUITETURA_DETALHES.py)** - Análise profunda (30 min)
   - Cada camada em detalhes
   - Implementações concretas
   - Testabilidade
   - Benefícios práticos

### Para Explorar o Código
5. **[ESTRUTURA_PROJETO.py](ESTRUTURA_PROJETO.py)** - Estrutura de pastas (15 min)
   - Árvore completa
   - Arquivo por arquivo
   - Localização de cada componente
   - Tecnologias por camada

6. **[VISUALIZAR_ESTRUTURA.py](VISUALIZAR_ESTRUTURA.py)** - Visualização ASCII (5 min)
   - Árvore visual
   - Dependency flow
   - Entry points
   - File statistics

### Para Usar a API
7. **[EXEMPLOS_USO.sh](EXEMPLOS_USO.sh)** - Exemplos de requisições (10 min)
   - Registrar paciente
   - Criar problema (RCOP)
   - Registrar SOAP
   - Fluxo completo
   - Testes de erro

## 🚀 Quick Start (escolha seu SO)

### Windows
```batch
cd prontuarioeletronico
quickstart.bat
```

### Linux / macOS
```bash
cd prontuarioeletronico
bash quickstart.sh
```

### Docker
```bash
docker-compose up --build
curl http://localhost:8000/docs
```

## 📂 Estrutura de Documentos

```
prontuarioeletronico/
├── README.md                      ← COMECE AQUI (Overview)
├── GUIA_RAPIDO.md                 ← Referência rápida
├── ARQUITETURA_VISUAL.py          ← Diagrama ASCII Art
├── ARQUITETURA_DETALHES.py        ← Análise profunda
├── ESTRUTURA_PROJETO.py           ← Estrutura de pastas detalhada
├── VISUALIZAR_ESTRUTURA.py        ← Árvore visual
├── EXEMPLOS_USO.sh                ← Exemplos de requisições API
├── INDICE_DOCUMENTACAO.md         ← Este arquivo
│
├── requirements.txt               ← Dependências
├── Dockerfile                     ← Container
├── docker-compose.yaml            ← Orquestração local
├── quickstart.sh / .bat           ← Start scripts
├── tests.py                       ← Testes unitários
│
└── src/                           ← CÓDIGO FONTE
    ├── domain/                    ← Camada 1: Entidades
    ├── application/               ← Camada 2: Casos de Uso
    └── infra/                     ← Camadas 3 & 4: API + DB
```

## 🧬 Entidades Principais

| Entidade | Arquivo | Descrição |
|----------|---------|-----------|
| `Patient` | `src/domain/patient/patient_entity.py` | Dados do paciente |
| `Professional` | `src/domain/professional/professional_entity.py` | Profissional de saúde |
| `Problem` | `src/domain/clinical_record/rcop_soap.py` | Problema clínico (RCOP) |
| `ClinicalRecord` | `src/domain/clinical_record/rcop_soap.py` | Registro (SOAP) |
| `Subjective, Objective, Assessment, Plan` | `src/domain/clinical_record/rcop_soap.py` | Componentes SOAP |
| `Appointment` | `src/domain/appointment/appointment_entity.py` | Agendamento |

## 📊 Casos de Uso Implementados

| Caso de Uso | Arquivo | Input | Output |
|-------------|---------|-------|--------|
| Registrar Paciente | `src/application/patient/register_patient_usecase.py` | PatientDTO | patient_id |
| Criar Problema | `src/application/clinical_record/create_problem_usecase.py` | ProblemDTO | problem_id |
| Registrar SOAP | `src/application/clinical_record/register_soap_usecase.py` | SOAPDTO | record_id |
| Agendar Consulta | `src/application/appointment/schedule_appointment_usecase.py` | AppointmentDTO | appointment_id |

## 🔗 URLs Principais

| Elemento | URL/Local |
|----------|-----------|
| **API Root** | `http://localhost:8000/` |
| **Swagger UI** | `http://localhost:8000/docs` |  
| **ReDoc** | `http://localhost:8000/redoc` |
| **Health Check** | `http://localhost:8000/health` |
| **Info API** | `http://localhost:8000/api/v1` |

## 📡 Endpoints Disponíveis

```
POST   /api/v1/patients/                    Registrar paciente
GET    /api/v1/patients/{id}                Consultar paciente
GET    /api/v1/patients/                    Listar pacientes
POST   /api/v1/clinical-records/problems    Criar problema
POST   /api/v1/clinical-records/soap        Registrar SOAP
```

## 🧪 Como Testar

### Testes Unitários
```bash
python -m pytest tests.py -v
python -m pytest tests.py --cov=src
```

### Testes Manuais (cURL)
```bash
# Registrar paciente
curl -X POST http://localhost:8000/api/v1/patients/ \
  -H "Content-Type: application/json" \
  -d '{"name": "João", ...}'

# Listar pacientes
curl http://localhost:8000/api/v1/patients/
```

## 🏗️ Camadas Explicadas

### Camada 1: Entidades (src/domain/)
- **Função**: Encapsular regras clinicamente corretas
- **Independência**: Nenhuma dependência externa
- **Exemplos**: Patient, Problem, ClinicalRecord, SOAP
- **Estabilidade**: Raramente muda (10-20 anos)

### Camada 2: Casos de Uso (src/application/)
- **Função**: Orquestrar fluxo de negócio
- **Conhecimento**: Domain layer apenas
- **Exemplos**: RegisterPatientUseCase, RegisterSOAPUseCase
- **Mudança**: Quando regras de negócio mudam

### Camada 3: Adaptadores (src/infra/api/)
- **Função**: Converter HTTP ↔ Use Case
- **Componentes**: Controllers, DTOs (Presenters)
- **Tecnologia**: FastAPI + Pydantic
- **Mudança**: Quando interface muda

### Camada 4: Drivers (src/infra/*/sqlalchemy/)
- **Função**: Persistência e frameworks
- **Componentes**: Models ORM, Repositories, Config
- **Technologia**: SQLAlchemy, SQLite/PostgreSQL
- **Mudança**: Frequente (detalhes técnicos)

## 💡 Princípios Implementados

### ✓ Regra da Dependência
- Dependências sempre apontam para dentro
- Domain não conhece nada externo
- Inversão de controle (injeção de dependência)

### ✓ Isolamento de Responsabilidades
- Cada camada tem responsabilidade clara
- Mudanças localizadas
- Reutilização sem efeitos colaterais

### ✓ Testabilidade
- Domain testável sem DB ou HTTP
- Use cases testável com mock
- APIs testável com cliente

### ✓ Independência Tecnológica
- Banco de dados é detalhe
- Framework web é detalhe
- Lógica clínica é essência

## 🎓 Conceitos Chave

| Conceito | Implementação |
|----------|---------------|
| **Entity** | Classes em `domain/` com regras de negócio |
| **Use Case** | Classes que herdam de `UseCase<Input, Output>` |
| **DTO** | Pydantic models para transferência de dados |
| **Repository** | Interface em domain, implementação em infra |
| **Presenter** | Camada de apresentação (adapta response) |
| **Adapter** | Controllers que convertem HTTP para use cases |

## 📈 Próximas Etapas

1. **Autenticação & Autorização**
   - JWT tokens
   - Role-based access control

2. **Mais Casos de Uso**
   - Update/Delete operations
   - Search e filtering
   - History and evolution

3. **Validação Avançada**
   - Regras clínicas customizadas
   - Alertas de segurança
   - Quality checks

4. **Integração IA**
   - Sugestão diagnóstica
   - Análise de risco
   - MLOps

5. **Conformidade**
   - LGPD compliance
   - Auditoria
   - Criptografia

## 🔗 Aprenda Mais

- **Clean Architecture Book**: "Clean Architecture" by Robert C. Martin
- **Design Patterns**: Gang of Four patterns
- **DDD**: Domain-Driven Design concepts
- **SOLID**: S.O.L.I.D principles

## 📞 Suporte

Para dúvidas sobre:
- **Arquitetura**: Leia ARQUITETURA_VISUAL.py e ARQUITETURA_DETALHES.py
- **Estrutura**: Leia ESTRUTURA_PROJETO.py
- **Uso**: Leia EXEMPLOS_USO.sh
- **Quick Reference**: Leia GUIA_RAPIDO.md

## ✨ Status

- ✅ Domain layer (7 entities)
- ✅ Application layer (4 use cases)
- ✅ Infrastructure layer (API + DB)
- ✅ Docker configuration
- ✅ Unit tests
- ✅ Documentation (6 guides)
- 🔄 Authentication (TODO)
- 🔄 More endpoints (TODO)
- 🔄 Integration tests (TODO)

---

**Última atualização**: Fevereiro 2024  
**Versão**: 1.0.0 - Protótipo Funcional  
**Status**: Pronto para produção com adições de segurança

