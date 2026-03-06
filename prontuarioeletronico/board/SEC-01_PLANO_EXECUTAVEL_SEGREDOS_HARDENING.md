# SEC-01 — Plano Executável (Gestão de Segredos e Hardening Inicial)

- **Data de abertura:** 2026-03-06
- **Issue alvo:** #7 SEC-01 Gestão de segredos e hardening inicial
- **Objetivo:** estabelecer baseline de segurança para segredos e varredura automatizada sem achados críticos, mantendo testabilidade e contratos atuais.

---

## 1) Escopo de implementação

1. Hardening de configuração por ambiente nos serviços:
   - `auth-service`
   - `patient-service`
   - `gateway-service`
2. Garantir que em `production`/`staging` não haja fallback inseguro para endpoints/segredos críticos.
3. Definir padrões de variáveis de ambiente em arquivos de exemplo (`.env.example`) por serviço.
4. Adicionar job de segurança no CI para varredura de código com foco em achados críticos.
5. Atualizar documentação técnica e de board com evidências.

---

## 2) Entregáveis previstos

### Código
- ajustes de inicialização/env nos serviços
- `.env.example` em cada serviço

### CI
- novo job `security-baseline` em `.github/workflows/python-ci.yml`
- varredura `bandit` em severidade alta/critical equivalente

### Documentação
- relatório técnico de execução SEC-01
- atualização de backlog/board com status

---

## 3) Critérios de aceite

- [x] Segredos/URLs críticos sem fallback em produção.
- [x] Padrão de configuração por ambiente documentado.
- [x] Varredura de segurança automatizada no CI.
- [x] Execução sem achados críticos na baseline definida.
- [x] Testes principais (core/auth/patient/gateway) mantidos verdes.

---

## 4) Sequência de execução

1. Implementar hardening de env/config nos serviços.
2. Adicionar arquivos `.env.example` e documentação mínima de uso.
3. Integrar job de segurança no CI.
4. Rodar validações locais (testes + scan).
5. Registrar evidências e atualizar checklist.
