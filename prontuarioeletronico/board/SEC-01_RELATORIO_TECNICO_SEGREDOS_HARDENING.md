# SEC-01 — Relatório Técnico (Gestão de Segredos e Hardening Inicial)

- **Data de fechamento técnico:** 2026-03-06
- **Issue alvo:** #7 SEC-01 Gestão de segredos e hardening inicial
- **Objetivo:** estabelecer baseline de segurança para configuração de segredos e varredura automatizada com foco em achados críticos.

---

## 1) Escopo executado

1. Hardening de configuração por ambiente em `auth-service`, `patient-service` e `gateway-service`.
2. Remoção de dependência de fallback implícito para produção/staging em variáveis críticas.
3. Padronização de configuração via `.env.example` por serviço.
4. Inclusão de varredura de segurança automatizada no CI (`security-baseline`).

---

## 2) Mudanças técnicas realizadas

### 2.1 Auth Service

Arquivo atualizado:
- `services/auth-service/src/auth/infra/auth/database.py`

Ações:
- Adição de `APP_ENV` para decisões de hardening.
- Exigência de `AUTH_DATABASE_URL` em `production/staging`.
- Controle de bootstrap de usuários padrão via `AUTH_BOOTSTRAP_DEFAULT_USERS`.
- Restrição de bootstrap automático para ambientes `development/test`.

### 2.2 Patient Service

Arquivos atualizados:
- `services/patient-service/src/patient/infra/api/main.py`
- `services/patient-service/src/patient/infra/patient/database.py`

Ações:
- Exigência de `AUTH_SERVICE_URL` em `production/staging`.
- Exigência de `PATIENT_DATABASE_URL` em `production/staging`.
- Preservação de defaults locais para `development`.

### 2.3 Gateway Service

Arquivo atualizado:
- `services/gateway-service/src/gateway/infra/api/main.py`

Ações:
- Exigência de `AUTH_SERVICE_URL` e `PATIENT_SERVICE_URL` em `production/staging`.
- Preservação de defaults locais para `development`.

### 2.4 Padronização de ambiente

Arquivos criados:
- `services/auth-service/.env.example`
- `services/patient-service/.env.example`
- `services/gateway-service/.env.example`

Ações:
- Definição explícita de variáveis obrigatórias por ambiente.
- Referência de configuração mínima para execução segura.

### 2.5 Segurança no CI

Arquivo atualizado:
- `.github/workflows/python-ci.yml`

Ações:
- Criação do job `security-baseline`.
- Varredura com `bandit` para serviços (`auth`, `patient`, `gateway`) em severidade e confiança altas (`-lll -iii`).

---

## 3) Evidências de documentação

- Plano executável: `board/SEC-01_PLANO_EXECUTAVEL_SEGREDOS_HARDENING.md`
- Este relatório: `board/SEC-01_RELATORIO_TECNICO_SEGREDOS_HARDENING.md`
- READMEs dos serviços atualizados com seção de hardening SEC-01.

---

## 4) Critérios de aceite (resultado)

- [x] Segredos/URLs críticos sem fallback em produção.
- [x] Padrão de configuração por ambiente documentado.
- [x] Varredura de segurança automatizada no CI.
- [x] Baseline sem achados críticos na varredura configurada.
- [x] Testabilidade preservada no escopo principal dos serviços.

---

## 5) Conclusão

A SEC-01 foi implementada com foco em hardening inicial, padronização de configuração e controle automatizado de segurança em pipeline, sem ruptura dos contratos e da abordagem de testabilidade já adotada no projeto.
