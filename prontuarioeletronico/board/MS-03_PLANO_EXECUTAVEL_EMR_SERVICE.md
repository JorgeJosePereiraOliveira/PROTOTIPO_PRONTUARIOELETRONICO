# MS-03 — Plano Executável (EMR Service RCOP/SOAP)

- **Data de abertura:** 2026-03-09
- **Issue alvo:** #8 MS-03 Implementar EMR Service (RCOP/SOAP)
- **Objetivo:** disponibilizar operações RCOP/SOAP por API em microsserviço dedicado, com segurança JWT/RBAC, persistência SQLAlchemy, integração com gateway e validação em CI.

---

## 1) Escopo mínimo vertical

1. Criar `emr-service` no padrão ARC-02 adotado.
2. Implementar domínio clínico mínimo:
   - `Problem` (RCOP)
   - `SOAPRecord` (registro SOAP)
3. Expor endpoints básicos:
   - `POST /api/v1/emr/problems`
   - `GET /api/v1/emr/problems/{problem_id}`
   - `POST /api/v1/emr/soap`
   - `GET /api/v1/emr/soap/{soap_id}`
4. Integrar segurança com `auth-service` (verify/authorize) e RBAC (`admin`, `profissional`).
5. Persistir dados em SQLAlchemy.
6. Cobrir com testes:
   - API funcional
   - contrato OpenAPI
   - E2E via gateway com token real
7. Integrar no CI.

---

## 2) Critérios de aceite da MS-03

- [x] Operações RCOP/SOAP disponíveis por API.
- [x] Segurança JWT/RBAC aplicada.
- [x] Persistência SQLAlchemy funcional.
- [x] Testes de contrato aprovados.
- [x] E2E via gateway aprovado.
- [x] Pipeline CI com suíte do EMR service.

---

## 3) Entregáveis previstos

- `services/emr-service/` (código + testes + README + .env.example)
- atualização em `services/gateway-service` para proxy de EMR
- atualização em `.github/workflows/python-ci.yml`
- relatório técnico de execução da MS-03 no board
