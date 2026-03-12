# MS-06 - Plano Executavel (Professional Service)

- **Data de abertura:** 2026-03-12
- **Issue alvo:** #32 MS-06 Implementar Professional Service
- **Objetivo:** implementar microsservico dedicado ao cadastro e consulta de profissionais de saude (medicos, enfermeiros e correlatos), com integracao via gateway, seguranca JWT/RBAC e trilha de auditoria.

---

## 1) Contexto e justificativa

A arquitetura atual possui servicos de autenticacao, paciente, prontuario, agendamento e auditoria, porem sem um contexto dedicado para identidade profissional assistencial. Isso gera risco de acoplamento entre identidade tecnica (usuario autenticado) e identidade clinica (profissional habilitado), reduzindo rastreabilidade e governanca.

A MS-06 fecha esse gap introduzindo o `professional-service` como bounded context proprio, aderente a Clean Architecture e pronto para evolucoes de autorizacao contextual, compliance e interoperabilidade.

---

## 2) Escopo minimo da primeira fatia (vertical)

1. Criar `professional-service` no padrao ARC-02 (domain/application/infra/tests).
2. Modelar entidade de dominio `Professional` com identificacao profissional e estado de ativacao.
3. Implementar casos de uso minimos:
   - registrar profissional;
   - buscar por id;
   - listar com filtros basicos;
   - ativar/desativar profissional.
4. Publicar endpoints no `professional-service`:
   - `POST /api/v1/professionals`
   - `GET /api/v1/professionals/{professional_id}`
   - `GET /api/v1/professionals`
   - `POST /api/v1/professionals/{professional_id}/deactivate`
   - `POST /api/v1/professionals/{professional_id}/activate`
5. Integrar seguranca JWT/RBAC via `auth-service`.
6. Integrar auditoria no `audit-service` para eventos criticos de cadastro e mudanca de status.
7. Publicar proxies equivalentes no `gateway-service`.
8. Cobrir com testes de servico, contrato OpenAPI e integracao gateway.
9. Atualizar CI para incluir `professional-service-tests` e guardrails de compatibilidade.
10. Publicar documentacao tecnica no board (plano + relatorio de fechamento da issue).

---

## 3) Contrato inicial da API (MVP)

### 3.1 Registrar profissional
- **POST** `/api/v1/professionals`
- Payload minimo:
  - `full_name` (string, obrigatorio)
  - `document_cpf` (string, obrigatorio)
  - `council_type` (string, obrigatorio) ex.: `CRM`, `COREN`, `CRO`
  - `council_uf` (string, obrigatorio)
  - `council_number` (string, obrigatorio)
  - `occupation` (string, obrigatorio) ex.: `medico`, `enfermeiro`
  - `specialty` (string, opcional)
  - `auth_user_id` (string, opcional na fatia 1)
- Retorno: `201` com profissional criado.

### 3.2 Buscar profissional por id
- **GET** `/api/v1/professionals/{professional_id}`
- Retorno: `200` quando encontrado, `404` quando inexistente.

### 3.3 Listar profissionais
- **GET** `/api/v1/professionals`
- Query params minimos:
  - `council_type`
  - `council_uf`
  - `council_number`
  - `status` (`active|inactive`)
- Retorno: `200` com lista.

### 3.4 Ativar/desativar profissional
- **POST** `/api/v1/professionals/{professional_id}/deactivate`
- **POST** `/api/v1/professionals/{professional_id}/activate`
- Retorno: `200` com status atualizado.

---

## 4) Regras de negocio da fatia inicial

- Nao permitir duplicidade de registro profissional por `council_type + council_uf + council_number`.
- `full_name`, `occupation`, `document_cpf` e dados de conselho sao obrigatorios para cadastro.
- Status inicial do profissional: `active`.
- Operacao de desativacao deve ser idempotente para profissional ja inativo.
- Operacao de ativacao deve ser idempotente para profissional ja ativo.
- Alteracoes de estado e cadastro devem gerar evento de auditoria (`create_professional`, `activate_professional`, `deactivate_professional`).
- Falha no envio de auditoria nao bloqueia operacao principal (fail-open com logging).

---

## 5) Integracoes obrigatorias

### 5.1 Gateway
- Publicar as rotas de borda em `gateway-service` com propagacao de token JWT.
- Preservar codigos HTTP e payload de erro do servico de origem.

### 5.2 Auth (JWT/RBAC)
- `POST` de cadastro e mudanca de status: papel `admin`.
- `GET` por id/lista: papeis `admin|profissional`.
- Em fatia futura, restringir profissional para leitura do proprio registro quando `auth_user_id` estiver vinculado.

### 5.3 Audit
- Integrar cliente HTTP ao `audit-service` para emissao de eventos de mudanca de estado.
- Registrar `actor_id`, `actor_role`, `resource_type=professional`, `resource_id`, `operation`, `status`, `metadata`.

---

## 6) Arquitetura e estrutura esperada

Estrutura alvo:
- `services/professional-service/src/professional/domain/professional/`
- `services/professional-service/src/professional/application/professional/`
- `services/professional-service/src/professional/infra/professional/`
- `services/professional-service/src/professional/infra/auth/`
- `services/professional-service/src/professional/infra/audit/`
- `services/professional-service/src/professional/infra/api/main.py`
- `services/professional-service/tests/`

Padroes obrigatorios:
- validacao de regras no use case;
- isolamento de HTTP clients em `infra`;
- persistencia via SQLAlchemy;
- funcao `_reset_for_tests()` para isolamento de testes.

---

## 7) Containerizacao, Kubernetes e CI/CD (alinhamento da fatia)

Mesmo com historias especificas de plataforma no backlog (DOCKER/K8S/CICD), esta fatia deve sair pronta para acoplamento operacional:

1. **Containerizacao (pronto para DOCKER-01):**
- incluir `Dockerfile` no `professional-service` com usuario nao-root e `HEALTHCHECK`.
- incluir `.env.example` com variaveis minimas do servico.

2. **Kubernetes (preparacao para K8S-01):**
- padronizar `health endpoint` (`/health`) e porta do servico.
- nome de app, labels e readiness/liveness compativeis com manifests padrao do projeto.

3. **CI/CD (preparacao para CICD-02):**
- adicionar job `professional-service-tests` no workflow existente.
- manter `api-compatibility-check` em verde.
- manter `security-baseline` sem regressao.

---

## 8) Sequencia executavel (passo a passo)

1. Scaffold do `professional-service` com template ARC-02.
2. Dominio `Professional` + interface de repositorio.
3. Use cases de `register`, `find`, `list`, `activate/deactivate`.
4. Persistencia SQLAlchemy e migracao leve (quando aplicavel).
5. API FastAPI + RBAC integrado ao `auth-service`.
6. Cliente de auditoria e eventos criticos.
7. Testes locais do `professional-service`.
8. Proxy no `gateway-service` + testes de integracao.
9. Atualizacoes no workflow de CI e checker de compatibilidade.
10. Evidencias na issue #32 + relatorio tecnico da MS-06.

---

## 9) Criterios de aceite da fatia

- [ ] `professional-service` criado no padrao arquitetural do projeto.
- [ ] Cadastro e consulta de profissional operacionais por API.
- [ ] Regras de unicidade de conselho aplicadas.
- [ ] Ativacao/desativacao operacional com rastreabilidade.
- [ ] Integracao via gateway funcional.
- [ ] Integracao com auditoria funcional para eventos criticos.
- [ ] Suites de testes relevantes em verde (`professional-service` + `gateway-service`).
- [ ] `api-compatibility-check` sem breaking change nao planejada.
- [ ] baseline de CI em `main` com checks obrigatorios em `success`.

---

## 10) Evidencia esperada de encerramento da fatia

No fechamento tecnico da issue #32, registrar:
- commit(s) principais da entrega;
- resultado de `pytest -q tests` no `professional-service`;
- resultado de testes de gateway relacionados;
- resultado do checker de compatibilidade de API;
- run final de referencia em `main` (id + URL + status);
- links para:
  - este plano executavel;
  - relatorio tecnico da MS-06.
