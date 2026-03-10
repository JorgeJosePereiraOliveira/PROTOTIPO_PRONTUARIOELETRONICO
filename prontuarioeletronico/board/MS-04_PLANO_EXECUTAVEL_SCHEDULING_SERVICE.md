# MS-04 — Plano Executável (Scheduling Service)

- **Data de abertura:** 2026-03-10
- **Issue alvo:** MS-04 Implementar Scheduling Service
- **Objetivo:** disponibilizar um microsserviço de agendamento desacoplado, com segurança JWT/RBAC, persistência SQLAlchemy, integração via gateway e validação completa em CI.

---

## 1) Contexto e justificativa

A entrega MS-03 consolidou o contexto clinico (EMR RCOP/SOAP). O próximo passo natural no backlog Sprint 3 e a separacao do contexto de agenda, reduzindo acoplamento entre fluxo clinico e fluxo operacional de consultas.

Com o `scheduling-service`, o sistema passa a ter:
- contexto dedicado para disponibilidade e agenda;
- evolucao independente das regras de agendamento;
- base para futuras regras de conflito, cancelamento e remarcacao.

---

## 2) Escopo minimo vertical (entrega desta issue)

1. Gerar `scheduling-service` no padrao arquitetural vigente (ARC-02).
2. Implementar dominio minimo de agendamento (`Appointment`).
3. Expor endpoints basicos:
   - `POST /api/v1/scheduling/appointments`
   - `GET /api/v1/scheduling/appointments/{appointment_id}`
   - `GET /api/v1/scheduling/appointments`
   - `DELETE /api/v1/scheduling/appointments/{appointment_id}`
4. Aplicar seguranca JWT/RBAC via `auth-service`:
   - leitura e criacao: `admin` e `profissional`
   - exclusao: `admin`
5. Implementar persistencia SQLAlchemy com banco proprio.
6. Cobrir com testes:
   - API funcional
   - contrato OpenAPI
   - E2E de autorizacao com token real
   - E2E via gateway (auth + scheduling)
7. Integrar no CI (job dedicado + compatibilidade + security baseline).

---

## 3) Contratos iniciais da API

### 3.1 Criar agendamento
- **POST** `/api/v1/scheduling/appointments`
- Payload inicial:
  - `patient_id` (string)
  - `professional_id` (string)
  - `scheduled_at` (string ISO-8601)
  - `reason` (string)
- Retorno: `201` com objeto do agendamento.

### 3.2 Buscar por id
- **GET** `/api/v1/scheduling/appointments/{appointment_id}`
- Retorno: `200` quando encontrado, `404` quando inexistente.

### 3.3 Listar
- **GET** `/api/v1/scheduling/appointments`
- Retorno: `200` com lista de agendamentos.

### 3.4 Cancelar/remover
- **DELETE** `/api/v1/scheduling/appointments/{appointment_id}`
- Retorno: `200` com `{"deleted": true}` quando removido, `404` quando inexistente.

---

## 4) Arquitetura alvo da entrega

Estrutura esperada:
- `services/scheduling-service/src/scheduling/domain/scheduling/`
- `services/scheduling-service/src/scheduling/application/scheduling/`
- `services/scheduling-service/src/scheduling/infra/scheduling/`
- `services/scheduling-service/src/scheduling/infra/auth/`
- `services/scheduling-service/src/scheduling/infra/api/main.py`
- `services/scheduling-service/tests/`

Padroes obrigatorios:
- Validacoes no use case.
- Dependencias externas isoladas na camada `infra`.
- `_reset_for_tests()` para isolamento entre testes.

---

## 5) Sequencia executavel (passo a passo)

1. Scaffold do novo servico a partir do template.
2. Dominio + interfaces de repositorio.
3. Use cases de criar, buscar, listar e excluir agendamento.
4. Infra SQLAlchemy (base, models, database, repositories).
5. API FastAPI com RBAC integrado ao `auth-service`.
6. Testes locais do `scheduling-service`.
7. Integracao no `gateway-service` com rotas proxy de scheduling.
8. Testes de integracao do gateway com fluxo auth+scheduling.
9. Atualizacao de CI:
   - novo job `scheduling-service-tests`
   - inclusao em security baseline
   - inclusao na verificacao de compatibilidade de API
10. Atualizacao documental e relatorio tecnico da MS-04.

---

## 6) Criterios de aceite da MS-04

- [x] `scheduling-service` criado e funcional no padrao arquitetural.
- [x] Endpoints de agendamento publicados e documentados no OpenAPI.
- [x] JWT/RBAC aplicado conforme perfis definidos.
- [x] Persistencia SQLAlchemy operacional.
- [x] Testes de contrato e testes E2E aprovados.
- [x] Gateway integrado com rotas de scheduling.
- [x] Pipeline CI com suite do scheduling e checks verdes no baseline de `main`.

---

## 7) Entregaveis esperados

- `services/scheduling-service/` (codigo, testes, README, `.env.example`).
- Atualizacoes em `services/gateway-service` para proxy de scheduling.
- Atualizacoes em `.github/workflows/python-ci.yml`.
- Atualizacao em `contracts/api_compatibility_baseline.json`.
- Atualizacao em `scripts/check_api_breaking_changes.py`.
- Relatorio tecnico de fechamento da MS-04 no board.

---

## 8) Riscos e mitigacoes

1. **Conflito de regras de data/hora:**
- Mitigacao: validar formato ISO-8601 e padronizar timezone no input.

2. **Acoplamento indevido com EMR/patient internamente:**
- Mitigacao: manter somente ids de referencia no contexto de scheduling.

3. **Instabilidade de import em CI entre servicos:**
- Mitigacao: manter padrao consolidado (`working-directory`, `PYTHONPATH`, `python -m pytest`).

---

## 9) Evidencia de encerramento (template)

No fechamento tecnico da issue MS-04, registrar:
- links dos commits principais;
- link do run baseline em `main` com checks obrigatorios em `success`;
- resumo objetivo de testes executados;
- referencias para plano e relatorio tecnico da MS-04.
