"""
VISUAL ASCII ART - CLEAN ARCHITECTURE DO PRONTUÁRIO ELETRÔNICO
Representação gráfica da arquitetura em anéis concêntricos
"""

ASCII_ARCHITECTURE = r"""

╔════════════════════════════════════════════════════════════════════════════╗
║           PRONTUÁRIO ELETRÔNICO - CLEAN ARCHITECTURE                      ║
║                    (Anéis Concêntricos)                                   ║
╚════════════════════════════════════════════════════════════════════════════╝


                              CAMADA 4
                    ╔═══════════════════════╗
                    ║  FRAMEWORKS & DRIVERS ║  🔴 VERMELHO
                    ║  (Detalhes Externos)  ║
                    ║                       ║
                    ║  • FastAPI            ║
                    ║  • SQLAlchemy         ║
                    ║  • SQLite/PostgreSQL  ║
                    ║  • Docker             ║
                    ║                       ║
                    ║ src/infra/api/main.py ║
                    ║ src/infra/api/config  ║
                    ║ src/infra/*/sqlalchemy║
                    ╚═══════════════════════╝
                            △ △ △ △ △ △ △ △
                    ╔═════════════════════════════╗
                    ║    CAMADA 3: ADAPTADORES    ║  🟢 VERDE
                    ║   (Interface Adapters)      ║
                    ║                             ║
                    ║  Controllers / Routers:     ║
                    ║  • patient_routers.py       ║
                    ║  • clinical_record_routers  ║
                    ║                             ║
                    ║  Request/Response DTOs:     ║
                    ║  • *_presenter.py           ║
                    ║                             ║
                    ║  Repositories (interfaces)  ║
                    ║  • *_repository_interface   ║
                    ╚═════════════════════════════╝
                          △ △ △ △ △ △ △ △ △ △
                    ╔═════════════════════════════╗
                    ║    CAMADA 2: CASOS DE USO    ║  🟡 AMARELO
                    ║   (Regras da Aplicação)     ║
                    ║                             ║
                    ║  Use Cases:                 ║
                    ║  • RegisterPatientUseCase   ║
                    ║  • CreateProblemUseCase     ║
                    ║  • RegisterSOAPUseCase      ║
                    ║  • ScheduleAppointmentUC    ║
                    ║                             ║
                    ║  Entrada/Saída:             ║
                    ║  • *InputDTO                ║
                    ║  • *OutputDTO               ║
                    ║                             ║
                    ║ src/application/*/          ║
                    ╚═════════════════════════════╝
                        △ △ △ △ △ △ △ △ △ △ △ △
                    ╔═════════════════════════════╗
                    ║   CAMADA 1: ENTIDADES       ║  🔵 AZUL
                    ║  (Regras de Negócio        ║
                    ║   RCOP/SOAP)                ║
                    ║                             ║
                    ║  Entidades Clínicas:       ║
                    ║  • Patient (paciente)       ║
                    ║  • Professional (prof)      ║
                    ║  • Problem (problema)       ║
                    ║  • ClinicalRecord (SOAP)    ║
                    ║  • Subjective (S)           ║
                    ║  • Objective (O)            ║
                    ║  • Assessment (A)           ║
                    ║  • Plan (P)                 ║
                    ║  • Appointment (consulta)   ║
                    ║                             ║
                    ║  Base Classes:              ║
                    ║  • Entity (base)            ║
                    ║  • UseCase interface        ║
                    ║  • Repository interface     ║
                    ║                             ║
                    ║ src/domain/*/               ║
                    ╚═════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════════

LEGEND:
  🔴 CAMADA 4: Frameworks & Drivers (VERMELHO)
     └─ Pode mudar frequentemente
     └─ Detalhes de implementação
     └─ Não afeta o núcleo

  🟢 CAMADA 3: Adaptadores (VERDE)
     └─ Converte HTTP ↔ Use Case ↔ Database
     └─ Controllers, DTOs, Presenters
     └─ Muda moderadamente

  🟡 CAMADA 2: Casos de Uso (AMARELO)
     └─ Orquestra fluxo de dados
     └─ Regras específicas da aplicação
     └─ Muda quando negócio muda

  🔵 CAMADA 1: Entidades (AZUL)
     └─ Nunca muda
     └─ Núcleo clínico (RCOP/SOAP)
     └─ Estável por décadas

═══════════════════════════════════════════════════════════════════════════════

REGRA DE DEPENDÊNCIA:

   Inner rings NUNCA conhecem Outer rings
   ↓↓↓ Dependências apontam SEMPRE para dentro ↓↓↓

   src/infra/ (externos)
       ↓   imports
   src/application/ (casos de uso)
       ↓   imports
   src/domain/ (núcleo)
       ↓
   Nada externo aqui! ✓

   ✗ NUNCA: domain imports application
   ✗ NUNCA: domain imports infra
   ✗ NUNCA: application imports implementation details of infra

═══════════════════════════════════════════════════════════════════════════════

FLUXO DE REQUISIÇÃO HTTP:

    HTTP Client
         │ POST /api/v1/patients/ + JSON
         ↓
    ┌──────────────────────────────────────┐
    │ LAYER 4: FastAPI Router              │
    │ patient_routers.py                   │
    │                                      │
    │ Recebe: HTTP Request                 │
    │ Retorna: HTTP Response               │
    └──────────────────┬───────────────────┘
                       │ chama
                       ↓
    ┌──────────────────────────────────────────────────┐
    │ LAYER 3: Presenter (Pydantic Validation)         │
    │ PatientCreateRequest                             │
    │                                                  │
    │ Valida JSON input                                │
    │ Deserializa para Python object                   │
    └──────────────────┬───────────────────────────────┘
                       │ passa para
                       ↓
    ┌──────────────────────────────────────────────────┐
    │ LAYER 2: Use Case                                │
    │ RegisterPatientUseCase.execute()                 │
    │                                                  │
    │ 1. Valida entrada (regras de negócio)           │
    │ 2. Cria entidade Patient                         │
    │ 3. Chama repository.add(patient)                 │
    │ 4. Retorna OutputDTO                             │
    └──────────────────┬───────────────────────────────┘
                       │ creates and manipulates
                       ↓
    ┌──────────────────────────────────────────────────┐
    │ LAYER 1: Entity (Domain)                         │
    │ Patient(id, name, cpf, ...)                      │
    │                                                  │
    │ • Encapsula regras clínicas                      │
    │ • Valida estado da entidade                      │
    │ • Contém métodos de domínio                      │
    │   - calculate_age()                              │
    │   - update_contact_info()                        │
    └──────────────────┬───────────────────────────────┘
                       │ passed to
                       ↓
    ┌──────────────────────────────────────────────────┐
    │ LAYER 4: Repository (Database)                   │
    │ PatientRepository.add(patient)                   │
    │                                                  │
    │ • Converte Patient entity → PatientModel         │
    │ • Executa SQL INSERT                             │
    │ • Commit transaction                             │
    └──────────────────┬───────────────────────────────┘
                       │
                       ↓
    ┌──────────────────────────────────────────────────┐
    │ SQLite/PostgreSQL Database                       │
    │                                                  │
    │ INSERT INTO patients (id, name, cpf) VALUES ...  │
    └──────────────────┬───────────────────────────────┘
                       │
                       ↓
    ┌──────────────────────────────────────────────────┐
    │ Response travels back up the stack:              │
    │ OutputDTO → JSON → HTTP Response                 │
    │                                                  │
    │ HTTP 200 OK                                      │
    │ {                                                │
    │   "patient_id": "uuid-xxxx",                     │
    │   "message": "Patient registered successfully"   │
    │ }                                                │
    └──────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

MATRIZ DE RESPONSABILIDADES:

┌──────────────────┬──────────────┬────────────┬──────────────┐
│ Elemento         │ Conhece DB?  │ Conhece    │ Conhece      │
│                  │              │ HTTP?      │ Banco Dados? │
├──────────────────┼──────────────┼────────────┼──────────────┤
│ Entity (Domain)  │ NÃO ✓        │ NÃO ✓      │ NÃO ✓        │
│ UseCase          │ NÃO ✓        │ NÃO ✓      │ NÃO ✓*       │
│ Router           │ SIM          │ SIM ✓      │ Via Repo     │
│ Repository       │ SIM ✓        │ NÃO ✓      │ SIM ✓        │
│ Model ORM        │ SIM ✓        │ NÃO ✓      │ SIM ✓        │
├──────────────────┼──────────────┼────────────┼──────────────┤
│ Testabilidade    │ Excelente    │ Excelente  │ Excelente    │
│ Manutenibilidade │ Máxima       │ Alta       │ Média        │
│ Flexibilidade    │ Máxima       │ Alta       │ Média        │
└──────────────────┴──────────────┴────────────┴──────────────┘

* Via injeção de dependência (interface)

═══════════════════════════════════════════════════════════════════════════════

EXEMPLO CONCRETO: Registrar SOAP Note

Fluxo:
1. Médico submete SOAP via interface web
2. POST /api/v1/clinical-records/soap
3. RegisterSOAPRequest validado (Pydantic)
4. RegisterSOAPUseCase orquestra criação de:
   - Subjective entity (S)
   - Objective entity (O)
   - Assessment entity (A)
   - Plan entity (P)
5. ClinicalRecord agrega os 4 componentes
6. ClinicalRecordRepository persiste tudo
7. Componentes SOAP são salvos em tabelas separadas
8. Response retorna record_id

Mudança: Nova regra clínica adicionada
→ Modifica: src/domain/clinical_record/rcop_soap.py
→ Tudo mais continua funcionando!

Mudança: Trocar banco por MongoDB
→ Modifica: src/infra/clinical_record/mongodb/
→ Domain, Application, Routers intactos!

═══════════════════════════════════════════════════════════════════════════════

PROTEÇÃO DO RCOP/SOAP (Núcleo Clínico):

A estrutura dos componentes SOAP é a entidade mais importante.
Clean Architecture garante:

┌─────────────────────────────────────────────────────────────┐
│ Mudanças Tecnológicas (Externas):                           │
│ ✓ FastAPI → Django                                          │
│ ✓ SQLite → PostgreSQL → Cassandra                           │
│ ✓ Monolito → Microsserviços                                 │
│ ✓ REST → GraphQL                                            │
│                                                              │
│ Resultado: RCOP/SOAP NÃO MUDA! ✓                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Mudanças Clínicas (Internas):                               │
│ ✓ Novo campo em SOAP                                        │
│ ✓ Validação RCOP mais rigorosa                              │
│ ✓ Novo tipo de problema                                     │
│ ✓ Integração com IA                                         │
│                                                              │
│ Resultado: Mudança localizada em domain/ apenas! ✓          │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

CONCLUSÃO:

O Prontuário Eletrônico implementado em Clean Architecture garante:

1. ✓ Testabilidade total (sem DB, sem HTTP)
2. ✓ Independência tecnológica (trocar frameworks)
3. ✓ Estabilidade do núcleo clínico (RCOP/SOAP)
4. ✓ Evolução garantida (30+ anos sem quebra)
5. ✓ Escalabilidade real (microsserviços, cache, etc)
6. ✓ Conformidade LGPD (regras isoladas)
7. ✓ Auditoria facilitada (fluxo claro)
8. ✓ Colaboração de equipes (responsabilidades claras)

═══════════════════════════════════════════════════════════════════════════════
"""

print(ASCII_ARCHITECTURE)

# Versão expandida para impressão
if __name__ == "__main__":
    print("\n" * 2)
    print("=" * 80)
    print("Diagrama impresso com sucesso!")
    print("Execute este arquivo para visualizar a arquitetura")
    print("=" * 80)
