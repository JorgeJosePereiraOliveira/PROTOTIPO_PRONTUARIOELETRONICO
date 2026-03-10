# MS-05 - Plano Executavel (Audit Service)

- **Data de abertura:** 2026-03-10
- **Issue alvo:** #11 MS-05 Implementar Audit Service
- **Objetivo:** implementar microsservico de auditoria para registro de eventos criticos com rastreabilidade por usuario e operacao, alinhado ao criterio de aceite da issue no GitHub.

---

## 1) Contexto e justificativa

Com Auth, Patient, EMR, Scheduling e CLN-01 consolidados, o proximo incremento P0 e registrar trilha de auditoria transversal para operacoes criticas. Isso reduz risco operacional/regulatorio e prepara as proximas entregas de LGPD, observabilidade e evidencias do artigo.

O `audit-service` deve registrar quem fez, o que fez, quando fez, em qual contexto e com qual resultado.

---

## 2) Escopo minimo vertical (entrega desta issue)

1. Gerar `audit-service` no padrao ARC-02.
2. Implementar entidade de evento de auditoria (`AuditEvent`).
3. Expor endpoints minimos:
   - `POST /api/v1/audit/events`
   - `GET /api/v1/audit/events`
   - `GET /api/v1/audit/events/{event_id}`
4. Aplicar seguranca JWT/RBAC via `auth-service`.
5. Persistencia SQLAlchemy dedicada ao contexto de auditoria.
6. Filtros minimos de consulta por `actor_id`, `operation`, `from`, `to`.
7. Cobertura de testes (API, contrato OpenAPI e E2E).
8. Integracao no gateway e CI/compatibilidade/security baseline.

---

## 3) Contrato inicial da API (MVP)

### 3.1 Registrar evento de auditoria
- **POST** `/api/v1/audit/events`
- Campos minimos:
  - `actor_id` (string)
  - `actor_role` (string)
  - `context` (string) ex.: `patient|emr|scheduling|auth`
  - `operation` (string) ex.: `create|update|delete|read|login|logout`
  - `resource_type` (string)
  - `resource_id` (string)
  - `status` (string) ex.: `success|denied|error`
  - `occurred_at` (ISO-8601)
  - `metadata` (objeto opcional)
- Retorno: `201` com evento persistido.

### 3.2 Consultar eventos
- **GET** `/api/v1/audit/events`
- Query params:
  - `actor_id`
  - `operation`
  - `from`
  - `to`
- Retorno: `200` com lista ordenada por `occurred_at` desc.

### 3.3 Buscar por id
- **GET** `/api/v1/audit/events/{event_id}`
- Retorno: `200` quando encontrado, `404` quando inexistente.

---

## 4) Arquitetura alvo da entrega

Estrutura esperada:
- `services/audit-service/src/audit/domain/audit/`
- `services/audit-service/src/audit/application/audit/`
- `services/audit-service/src/audit/infra/audit/`
- `services/audit-service/src/audit/infra/auth/`
- `services/audit-service/src/audit/infra/api/main.py`
- `services/audit-service/tests/`

Padroes obrigatorios:
- validacao no use case;
- isolamento de dependencias externas em `infra`;
- `_reset_for_tests()` para isolamento de testes.

---

## 5) Sequencia executavel (passo a passo)

1. Scaffold do `audit-service`.
2. Dominio (`AuditEvent`) + interface de repositorio.
3. Use cases de `create`, `find`, `list` com filtros.
4. Infra SQLAlchemy (models, database, repository).
5. API FastAPI + RBAC (`admin` para leitura completa, `admin|profissional` para registro).
6. Testes locais do `audit-service`.
7. Integracao de rotas no gateway.
8. Testes de integracao gateway (auth + audit).
9. Atualizacao de CI:
   - novo job `audit-service-tests`;
   - inclusao no `security-baseline`;
   - inclusao no checker de compatibilidade de API.
10. Atualizacao documental e relatorio tecnico da MS-05.

---

## 6) Criterios de aceite da MS-05

- [ ] `audit-service` criado no padrao arquitetural.
- [ ] Registro de eventos criticos funcional.
- [ ] Consulta de auditoria por usuario/operacao funcional.
- [ ] Persistencia e filtros minimos operacionais.
- [ ] Cobertura de testes no servico e via gateway.
- [ ] CI/seguranca/compatibilidade atualizados sem regressao.
- [ ] Evidencia de run verde em `main`.

---

## 7) Testabilidade orientada ao escopo do projeto

Para manter coerencia com o estado real do repositrio e com o TCC:
- cada historia P0 deve sair com evidencia de:
  - teste de servico;
  - teste de gateway quando houver rota exposta;
  - compatibilidade de API;
  - baseline de CI em `main`.
- logs de teste e links de run devem ser referenciados no relatorio tecnico.

---

## 8) Entregaveis esperados

- `services/audit-service/` (codigo, testes, README, `.env.example`, Dockerfile).
- atualizacoes em `services/gateway-service/` para proxy de auditoria.
- atualizacoes em `.github/workflows/python-ci.yml`.
- atualizacoes em `contracts/api_compatibility_baseline.json` e `scripts/check_api_breaking_changes.py`.
- relatorio tecnico de fechamento:
  - `board/MS-05_RELATORIO_TECNICO_AUDIT_SERVICE.md`.

---

## 9) Evidencia de encerramento (template)

No fechamento tecnico da issue #11, registrar:
- commits principais da entrega;
- run de referencia em `main` com checks obrigatorios em `success`;
- resultados de testes (`audit-service`, `gateway`, `compatibilidade`);
- links para plano e relatorio tecnico da MS-05.
