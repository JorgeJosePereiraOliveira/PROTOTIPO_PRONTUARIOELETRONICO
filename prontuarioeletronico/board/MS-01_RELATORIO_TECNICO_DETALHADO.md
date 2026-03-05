# MS-01 — Relatório Técnico Detalhado (Auth Service)

- **Data de fechamento técnico:** 2026-03-05
- **Issue:** MS-01 Implementar Auth Service (JWT + RBAC)
- **Repositório:** `JorgeJosePereiraOliveira/PROTOTIPO_PRONTUARIOELETRONICO`

---

## 1) Escopo executado

Este documento consolida, em sequência técnica, toda a execução realizada para o MS-01 no `auth-service`.

Objetivos cobertos:

1. Bootstrap de serviço real a partir do template ARC-02.
2. JWT + RBAC funcional (`admin` / `profissional`).
3. Persistência SQLAlchemy para usuários e estado de tokens.
4. Hardening de senha com `passlib` + `bcrypt`.
5. Segredo JWT obrigatório por ambiente (`AUTH_JWT_SECRET`).
6. Política de expiração/rotação com `refresh_token`.
7. Logout com revogação explícita e blacklist curta de `access_token`.
8. Testes de contrato OpenAPI (schema + exemplos de segurança) no pipeline.

---

## 2) Arquitetura entregue no Auth Service

Estrutura do serviço:

- `domain/`: entidades e contratos de domínio.
- `application/`: casos de uso de autenticação/autorização/token lifecycle.
- `infra/`: API FastAPI, JWT service, repositórios SQLAlchemy.

Componentes centrais:

- **Use cases**
  - `AuthenticateUserUseCase`
  - `AuthorizeRoleUseCase`
  - `RefreshAccessTokenUseCase`
  - `LogoutUseCase`
- **Infra token/security**
  - `JwtTokenService`
  - `BcryptPasswordHasher`
- **Persistência**
  - `SqlAlchemyUserRepository`
  - `SqlAlchemyRefreshTokenRepository`
  - `SqlAlchemyAccessTokenBlacklistRepository`

---

## 3) Linha do tempo técnica (passo a passo)

### 3.1 Bootstrap inicial do Auth Service

- Serviço criado via template ARC-02 em `services/auth-service`.
- Endpoints iniciais de health/info e testes base executados.

### 3.2 JWT + RBAC inicial

- Implementado login e validação de token.
- RBAC por papel clínico (`admin`, `profissional`) com endpoint de autorização.

### 3.3 Migração de repositório em memória para SQLAlchemy

- Substituição do `InMemoryUserRepository` por `SqlAlchemyUserRepository`.
- Bootstrap de usuários de desenvolvimento no banco.
- Ajuste de testes de contrato para usar SQLite em memória.

### 3.4 Hardening de senha e segredo obrigatório

- Troca de hash para `passlib + bcrypt`.
- `AUTH_JWT_SECRET` removido de fallback inseguro; obrigatório em qualquer ambiente.
- Compatibilização de versão `bcrypt==4.0.1` com `passlib==1.7.4` no ambiente atual.

### 3.5 Política de expiração + refresh token com rotação

- `access_token` com duração curta.
- `refresh_token` com duração longa.
- endpoint `POST /api/v1/auth/refresh` com rotação obrigatória.
- Persistência de estado por `jti` (revogação e substituição).

### 3.6 Logout e revogação explícita

- endpoint `POST /api/v1/auth/logout`.
- Revogação explícita de refresh token.
- Blacklist de access token por `jti` até `exp`.
- `verify` e `authorize` passaram a rejeitar token revogado.

### 3.7 Contrato OpenAPI no pipeline

- Teste de contrato OpenAPI criado para validar:
  - paths obrigatórios de auth;
  - esquema de segurança bearer no spec;
  - exemplos de payload e exemplos de respostas de segurança.
- CI atualizado para executar testes do `auth-service` (incluindo OpenAPI).

---

## 4) Endpoints finais do Auth Service

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/verify`
- `GET /api/v1/auth/authorize?required_role=<role>`
- `GET /health`
- `GET /api/v1/info`

---

## 5) Política de segurança e tokens

### 5.1 Password security

- Algoritmo: bcrypt via `passlib`.
- Credenciais de bootstrap apenas para desenvolvimento.

### 5.2 JWT policy

- `AUTH_JWT_SECRET` obrigatório no startup.
- `access_token` inclui `jti`, `type=access`, `exp` curta.
- `refresh_token` inclui `jti`, `type=refresh`, `exp` longa.

### 5.3 Rotation / revocation policy

- Refresh token só pode ser usado uma vez.
- Uso de refresh token causa rotação e revogação do token anterior.
- Logout revoga refresh token explicitamente.
- Access token do logout é colocado na blacklist até expirar.

---

## 6) Testes e validação executados

Coberturas implementadas:

1. Testes de API do fluxo de auth:
   - login
   - verify
   - authorize
   - refresh (inclui reutilização indevida)
   - logout com revogação + blacklist
2. Testes de casos de uso com SQLAlchemy.
3. Teste de contrato OpenAPI (schema + segurança).

Resultado final da suíte do auth-service no fechamento:

- `pytest -q` -> **10 passed**.

---

## 7) Integração no pipeline (CI)

Workflow atualizado:

- Job `core-tests`: executa `pytest -q prontuarioeletronico/src`.
- Job `auth-service-tests`: executa `pytest -q prontuarioeletronico/services/auth-service/tests`.

Com isso, o contrato OpenAPI do Auth Service passa a ser validado continuamente em PR/push.

---

## 8) Evidências de execução no board (issue comments)

Evidências registradas durante o MS-01:

- Bootstrap/Auth inicial: `#issuecomment-3998157683`
- SQLAlchemy migration: `#issuecomment-3998325865`
- Hardening (bcrypt + secret obrigatório): `#issuecomment-3999022134`
- Refresh rotation: `#issuecomment-4003869902`
- Logout + blacklist: `#issuecomment-4004005892`

Issue consolidada:

- `https://github.com/JorgeJosePereiraOliveira/PROTOTIPO_PRONTUARIOELETRONICO/issues/5`

---

## 9) Observações operacionais

1. Ambiente de teste define variáveis por `conftest.py` para execução determinística.
2. Artefatos SQLite locais (`auth.db`, `test_auth.db`) são tratados como não versionáveis.
3. Para produção, recomenda-se uso de banco gerenciado e rotação periódica de segredo JWT.

---

## 10) Critério de pronto do MS-01 (status)

- [x] Emissão e validação de JWT funcionando.
- [x] RBAC mínimo admin/profissional funcionando.
- [x] Health/readiness funcional.
- [x] Persistência real (SQLAlchemy) aplicada.
- [x] Hardening de senha e segredos aplicado.
- [x] Refresh token com rotação aplicado.
- [x] Logout com revogação explícita e blacklist aplicado.
- [x] Contrato OpenAPI validado por testes automatizados no pipeline.

**Status final:** MS-01 tecnicamente fechado e rastreado.
