# LGPD-01 - Plano Executavel (Consentimento e base legal)

- **Data de abertura:** 2026-03-11
- **Issue alvo:** #14 LGPD-01 Consentimento e base legal
- **Objetivo:** viabilizar registro e revogacao de consentimento do paciente com trilha de auditoria no ecossistema de microsservicos.

---

## 1) Contexto e justificativa

Com os fluxos clinicos estabilizados ate CLN-03, o proximo passo P0 e iniciar os controles de privacidade. Esta fatia introduz o ciclo minimo de consentimento (criar/revogar) com evidencia de auditoria para operacoes LGPD.

---

## 2) Escopo da primeira fatia (vertical)

1. Criar estrutura de consentimento no `patient-service` (dominio/aplicacao/infra).
2. Publicar endpoints de consentimento por paciente:
   - `POST /api/v1/patients/{patient_id}/consents`
   - `GET /api/v1/patients/{patient_id}/consents`
   - `POST /api/v1/patients/{patient_id}/consents/{consent_id}/revoke`
3. Integrar emissao de eventos no `audit-service` para criacao e revogacao.
4. Publicar proxy de consentimento no `gateway-service`.
5. Cobrir com testes de API, contrato OpenAPI e integracao.

---

## 3) Regras da fatia inicial

- Consentimento exige `legal_basis` e `purpose` validos.
- Nao permitir consentimento ativo duplicado por paciente+purpose.
- Revogacao exige consentimento existente e ativo.
- Operacoes devem gerar auditoria (`create_consent`, `revoke_consent`).
- Falha de auditoria nao bloqueia fluxo principal (fail-open).

---

## 4) Criterios de aceite da fatia

- [x] Consentimento criado com status `active`.
- [x] Consentimento revogado com status `revoked` e `revoked_at`.
- [x] Eventos de auditoria emitidos para criar/revogar.
- [x] Rotas correspondentes disponiveis no gateway.
- [x] Testes de API/contrato/integracao em verde.
- [x] Evidencia publicada na issue #14.

---

## 5) Evidencia esperada de encerramento da fatia

- commit com implementacao e testes;
- push em `main`;
- comentario na issue #14 com comandos e resultados de validacao.
