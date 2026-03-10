# MS-04 - Relatorio Tecnico (Scheduling Service)

- **Data de fechamento tecnico:** 2026-03-10
- **Issue alvo:** MS-04 Implementar Scheduling Service
- **Objetivo:** disponibilizar operacoes de agendamento por API em microsservico dedicado, com seguranca JWT/RBAC, persistencia SQLAlchemy, integracao com gateway e validacao em CI.

---

## 1) Escopo executado

1. Scaffold do `scheduling-service` no padrao ARC-02.
2. Implementacao do dominio minimo de agendamento (`Appointment`).
3. Exposicao dos endpoints planejados de create/get/list/delete em API v1.
4. Integracao de seguranca via `auth-service` com `verify/authorize` e RBAC (`admin`, `profissional`).
5. Persistencia com SQLAlchemy e banco configuravel por ambiente.
6. Cobertura de testes no `scheduling-service` (funcional e contrato OpenAPI).
7. Extensao do gateway para proxy de scheduling + testes de integracao e contrato.
8. Integracao de CI para o novo servico e atualizacao dos guardrails de seguranca/compatibilidade.

---

## 2) Mudancas tecnicas realizadas

### 2.1 Scheduling Service (dominio/aplicacao/infra)

Arquivos principais criados/atualizados:
- `services/scheduling-service/src/scheduling/domain/scheduling/appointment_entity.py`
- `services/scheduling-service/src/scheduling/domain/scheduling/appointment_repository_interface.py`
- `services/scheduling-service/src/scheduling/application/scheduling/create_appointment_usecase.py`
- `services/scheduling-service/src/scheduling/application/scheduling/find_appointment_usecase.py`
- `services/scheduling-service/src/scheduling/application/scheduling/list_appointments_usecase.py`
- `services/scheduling-service/src/scheduling/application/scheduling/delete_appointment_usecase.py`
- `services/scheduling-service/src/scheduling/infra/scheduling/sqlalchemy_base.py`
- `services/scheduling-service/src/scheduling/infra/scheduling/database.py`
- `services/scheduling-service/src/scheduling/infra/scheduling/sqlalchemy_models.py`
- `services/scheduling-service/src/scheduling/infra/scheduling/sqlalchemy_appointment_repository.py`
- `services/scheduling-service/src/scheduling/infra/auth/auth_service_client.py`
- `services/scheduling-service/src/scheduling/infra/api/main.py`

Resultados:
- Endpoints implementados:
  - `POST /api/v1/scheduling/appointments`
  - `GET /api/v1/scheduling/appointments/{appointment_id}`
  - `GET /api/v1/scheduling/appointments`
  - `DELETE /api/v1/scheduling/appointments/{appointment_id}`
- Seguranca RBAC aplicada nos endpoints de agendamento.
- Persistencia SQLAlchemy ativa com `SCHEDULING_DATABASE_URL` e configuracao por ambiente.

### 2.2 Testes do Scheduling Service

Arquivos criados:
- `services/scheduling-service/tests/test_scheduling_api.py`
- `services/scheduling-service/tests/test_openapi_contract.py`

Resultados:
- Testes funcionais de API cobrindo create/get/list/delete.
- Testes de contrato OpenAPI cobrindo paths e seguranca Bearer.

### 2.3 Gateway Service (proxy Scheduling)

Arquivos atualizados:
- `services/gateway-service/src/gateway/infra/api/main.py`
- `services/gateway-service/tests/test_gateway_integration.py`
- `services/gateway-service/tests/test_gateway_openapi_contract.py`

Resultados:
- Novas rotas proxy Scheduling no gateway:
  - `POST /api/v1/scheduling/appointments`
  - `GET /api/v1/scheduling/appointments/{appointment_id}`
  - `GET /api/v1/scheduling/appointments`
  - `DELETE /api/v1/scheduling/appointments/{appointment_id}`
- E2E gateway validando fluxo completo Auth + Scheduling.

### 2.4 CI, seguranca e compatibilidade de API

Arquivos atualizados:
- `.github/workflows/python-ci.yml`
- `scripts/check_api_breaking_changes.py`
- `contracts/api_compatibility_baseline.json`

Resultados:
- Novo job `scheduling-service-tests` no CI.
- Security baseline (`bandit`) expandido para `services/scheduling-service/src`.
- API compatibility checker atualizado para incluir `scheduling-service` e novas rotas Scheduling no gateway.

### 2.5 Documentacao e configuracao

Arquivos atualizados/criados:
- `services/scheduling-service/README.md`
- `services/scheduling-service/requirements.txt`
- `services/scheduling-service/.env.example`
- `board/MS-04_PLANO_EXECUTAVEL_SCHEDULING_SERVICE.md`

---

## 3) Evidencias de validacao

Execucoes realizadas:
1. `pytest -q tests` em `services/scheduling-service` -> **10 passed**.
2. `pytest -q tests` em `services/gateway-service` -> **7 passed**.
3. `python scripts/check_api_breaking_changes.py` -> **API compatibility check passed**.

Observacao:
- Foram emitidos warnings de deprecacao do `httpx` (`app shortcut`), sem impacto funcional no escopo MS-04.

---

## 4) Criterios de aceite (resultado)

- [x] `scheduling-service` criado e funcional no padrao arquitetural.
- [x] Endpoints de agendamento publicados e documentados no OpenAPI.
- [x] JWT/RBAC aplicado conforme perfis definidos.
- [x] Persistencia SQLAlchemy operacional.
- [x] Testes de contrato e testes E2E aprovados.
- [x] Gateway integrado com rotas de scheduling.
- [x] Pipeline CI com suite do scheduling e checks verdes no baseline de `main`.

---

## 5) Conclusao

A MS-04 foi implementada ponta a ponta no fluxo planejado: `scheduling-service` funcional com endpoints de agenda, seguranca integrada ao auth-service, persistencia SQLAlchemy, cobertura de testes em nivel de servico e gateway, e inclusao completa nos guardrails de CI, seguranca e compatibilidade de API.

---

## 6) Baseline de estabilidade (CI)

Para fins de governanca e rastreabilidade do TCC, adota-se como baseline operacional o ultimo commit em `main` com checks obrigatorios em status `success`.

- Commit baseline: `df797eac97c568f465de63062fc2ed2d69a4cd0a`
- Run de referencia no GitHub Actions: `22897129054`
- URL do run: `https://github.com/JorgeJosePereiraOliveira/PROTOTIPO_PRONTUARIOELETRONICO/actions/runs/22897129054`

Checks obrigatorios confirmados no baseline:
- `core-tests` -> success
- `auth-service-tests` -> success
- `patient-service-tests` -> success
- `emr-service-tests` -> success
- `scheduling-service-tests` -> success
- `gateway-integration-tests` -> success
- `api-compatibility-check` -> success
- `security-baseline` -> success

Nota de rastreabilidade:
- Runs historicos com `failure` foram preservados como evidencia da evolucao tecnica do projeto.
- Para aceite formal da issue, considera-se o baseline atual em `main` com checks obrigatorios verdes.
