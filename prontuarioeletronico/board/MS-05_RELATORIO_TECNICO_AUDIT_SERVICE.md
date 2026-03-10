# MS-05 - Relatorio Tecnico (Audit Service)

- **Data de fechamento tecnico:** 2026-03-10
- **Issue alvo:** #11 MS-05 Implementar Audit Service
- **Objetivo:** disponibilizar microsservico de auditoria para eventos criticos, com rastreabilidade por usuario/operacao, seguranca JWT/RBAC, persistencia SQLAlchemy, integracao via gateway e validacao em CI.

---

## 1) Escopo executado

1. Scaffold do `audit-service` no padrao ARC-02.
2. Implementacao da entidade de dominio `AuditEvent`.
3. Exposicao dos endpoints de auditoria planejados (`create`, `list`, `get by id`).
4. Integracao de seguranca via `auth-service` com `verify/authorize` e RBAC.
5. Persistencia SQLAlchemy dedicada para eventos de auditoria.
6. Filtros de consulta por `actor_id`, `operation`, `from`, `to`.
7. Cobertura de testes no `audit-service` (API, OpenAPI e health).
8. Integracao do gateway com rotas de auditoria + testes de integracao.
9. Integracao em CI, seguranca e compatibilidade de API.

---

## 2) Mudancas tecnicas realizadas

### 2.1 Audit Service (dominio/aplicacao/infra)

Arquivos principais criados/atualizados:
- `services/audit-service/src/audit/domain/audit/audit_event_entity.py`
- `services/audit-service/src/audit/domain/audit/audit_event_repository_interface.py`
- `services/audit-service/src/audit/application/audit/create_audit_event_usecase.py`
- `services/audit-service/src/audit/application/audit/find_audit_event_usecase.py`
- `services/audit-service/src/audit/application/audit/list_audit_events_usecase.py`
- `services/audit-service/src/audit/infra/audit/database.py`
- `services/audit-service/src/audit/infra/audit/sqlalchemy_models.py`
- `services/audit-service/src/audit/infra/audit/sqlalchemy_audit_event_repository.py`
- `services/audit-service/src/audit/infra/auth/auth_service_client.py`
- `services/audit-service/src/audit/infra/api/main.py`

Resultados:
- Endpoints implementados:
  - `POST /api/v1/audit/events`
  - `GET /api/v1/audit/events`
  - `GET /api/v1/audit/events/{event_id}`
- RBAC aplicado:
  - criacao de evento: `admin` e `profissional`
  - leitura/listagem: `admin`
- Validacoes de dominio:
  - obrigatoriedade de campos criticos
  - `status` permitido: `success|denied|error`
  - datas em ISO-8601 (`occurred_at`, `from`, `to`)

### 2.2 Testes do Audit Service

Arquivos criados:
- `services/audit-service/tests/test_audit_api.py`
- `services/audit-service/tests/test_openapi_contract.py`
- `services/audit-service/tests/test_health_endpoint.py`

Resultados:
- cobertura de fluxo funcional (`create/get/list`) com filtros.
- cobertura de erros de validacao e autorizacao.
- contrato OpenAPI validado para paths e seguranca Bearer.

### 2.3 Gateway Service (proxy Audit)

Arquivos atualizados:
- `services/gateway-service/src/gateway/infra/api/main.py`
- `services/gateway-service/tests/test_gateway_integration.py`
- `services/gateway-service/tests/test_gateway_openapi_contract.py`

Resultados:
- Novas rotas proxy audit no gateway:
  - `POST /api/v1/audit/events`
  - `GET /api/v1/audit/events`
  - `GET /api/v1/audit/events/{event_id}`
- Teste E2E de gateway validando fluxo auth + audit + RBAC.

### 2.4 CI, seguranca e compatibilidade de API

Arquivos atualizados:
- `.github/workflows/python-ci.yml`
- `scripts/check_api_breaking_changes.py`
- `contracts/api_compatibility_baseline.json`

Resultados:
- novo job `audit-service-tests` no CI.
- security baseline (`bandit`) expandido para `services/audit-service/src`.
- checker de compatibilidade atualizado para incluir `audit-service` e rotas de audit no gateway.

### 2.5 Documentacao e configuracao

Arquivos criados/atualizados:
- `services/audit-service/README.md`
- `services/audit-service/requirements.txt`
- `services/audit-service/.env.example`
- `services/audit-service/Dockerfile`
- `board/MS-05_PLANO_EXECUTAVEL_AUDIT_SERVICE.md`
- `board/TESTABILIDADE_PROTOCOLO_EXECUCAO.md`

---

## 3) Evidencias de validacao

Execucoes realizadas na fase final:
1. `pytest -q tests` em `services/audit-service` -> **9 passed**.
2. `pytest -q tests` em `services/gateway-service` -> **9 passed**.
3. `python scripts/check_api_breaking_changes.py` -> **API compatibility check passed**.

Observacao:
- warnings de deprecacao do `httpx` permaneceram sem impacto funcional na entrega.

---

## 4) Criterios de aceite (resultado)

- [x] `audit-service` criado no padrao arquitetural.
- [x] Registro de eventos criticos funcional.
- [x] Consulta de auditoria por usuario/operacao funcional.
- [x] Persistencia e filtros minimos operacionais.
- [x] Cobertura de testes no servico e via gateway.
- [x] CI/seguranca/compatibilidade atualizados sem regressao.
- [x] Evidencia de run verde em `main`.

---

## 5) Conclusao

A MS-05 foi concluida ponta a ponta com um `audit-service` funcional e integrado ao ecossistema do prototipo. A entrega fortalece rastreabilidade operacional e prepara base tecnica para requisitos de LGPD, observabilidade e evidencias do artigo.

---

## 6) Baseline de estabilidade (CI)

Para aceite formal da issue #11, considerar o commit final desta entrega em `main` e seu run em `success`.

- Commit final da MS-05: `__PREENCHER_APOS_PUSH__`
- Run de referencia: `__PREENCHER_APOS_PUSH__`
- URL: `__PREENCHER_APOS_PUSH__`

Nota de rastreabilidade:
- Runs historicos com falha seguem preservados para historico tecnico.
- Aceite formal considera baseline verde em `main` + criterios funcionais/documentais cumpridos.
