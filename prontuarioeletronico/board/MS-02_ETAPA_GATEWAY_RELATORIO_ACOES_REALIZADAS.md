# MS-02 — Etapa Gateway e Integração (Relatório de Ações Realizadas)

- **Data:** 2026-03-05
- **Objetivo do relatório:** registrar detalhadamente a implementação executada da etapa de integração por borda (Gateway), mantendo rastreabilidade para gestão, issue e banca/TCC.

---

## 1) Contexto e objetivo da execução

Com MS-01 (Auth Service) e MS-02 fase 2 (Patient Service) já concluídas, esta etapa teve como objetivo fechar a US-2.2 no nível de plataforma integrada, adicionando o `gateway-service` como borda única de consumo e validando o fluxo real de autenticação/autorização entre serviços.

---

## 2) Implementação realizada

### 2.1 Scaffold do gateway-service

- Serviço criado em `services/gateway-service` com estrutura padrão ARC-02.
- Ajustes de README e testes para foco em proxy/integração.

Arquivos principais:

- `services/gateway-service/README.md`
- `services/gateway-service/src/gateway/infra/api/main.py`
- `services/gateway-service/src/gateway/infra/proxy/http_service_proxy.py`

### 2.2 Rotas proxy para Auth e Patient

Rotas de auth implementadas no gateway:

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/verify`
- `GET /api/v1/auth/authorize`

Rotas de patient implementadas no gateway:

- `POST /api/v1/patients`
- `GET /api/v1/patients`
- `GET /api/v1/patients/{patient_id}`
- `PUT /api/v1/patients/{patient_id}`
- `DELETE /api/v1/patients/{patient_id}`

### 2.3 Propagação de segurança

- Cabeçalho `Authorization` propagado do gateway para serviços internos.
- Gateway não replica regra de negócio de segurança: delega a validação ao `auth-service` e ao `patient-service`.
- Resposta HTTP (status/body) do downstream é encaminhada de forma transparente.

### 2.4 Testes de integração via gateway

Arquivo criado:

- `services/gateway-service/tests/test_gateway_integration.py`

Cenários cobertos:

1. Login real via gateway com emissão de token.
2. CRUD de paciente por gateway com token válido.
3. RBAC real no delete:
   - `profissional` retorna `403`.
   - `admin` retorna `200`.
4. Token ausente/inválido retorna `401`.

### 2.5 Teste de contrato OpenAPI do gateway

Arquivo criado:

- `services/gateway-service/tests/test_gateway_openapi_contract.py`

Coberturas:

- presença de paths de auth/patient no spec;
- presença dos métodos esperados (POST/GET/PUT/DELETE);
- exemplo de schema para login.

### 2.6 Integração em CI

Arquivo atualizado:

- `.github/workflows/python-ci.yml`

Entrega:

- job `gateway-integration-tests` adicionado;
- instalação de dependências de gateway/auth/patient;
- execução de `pytest -q tests` no diretório do gateway.

---

## 3) Resultados de validação

Execuções locais realizadas após implementação:

- `gateway-service`: 5 testes aprovados.
- `auth-service`: 13 testes aprovados.

Esses resultados confirmam que o gateway integra corretamente os serviços existentes sem regressão funcional observada no escopo validado.

---

## 4) Atualização de governança

- Checklist do plano da etapa gateway atualizado para concluído em:
  - `board/MS-02_ETAPA_GATEWAY_PLANO_EXECUTAVEL.md`
- Navegação do board já inclui os artefatos da etapa:
  - `board/README_BOARD_EXECUCAO.md`

---

## 5) Conclusão

A etapa **Gateway + testes de integração + job de CI** foi implementada conforme plano, com rastreabilidade documental e validação automatizada, mantendo coerência com o escopo de fechamento integrado da US-2.2.
