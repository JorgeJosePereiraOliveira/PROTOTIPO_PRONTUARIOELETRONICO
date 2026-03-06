# ARC-03 — Relatório Técnico (Versionamento de APIs e Breaking Changes)

- **Data de fechamento técnico:** 2026-03-06
- **Issue alvo:** #3 ARC-03 Padronizar versionamento de APIs e breaking changes

---

## 1) Entregas realizadas

1. Política de versionamento de API publicada.
2. Baseline de compatibilidade de endpoints versionada no repositório.
3. Verificador automático de breaking changes implementado.
4. Integração da verificação no CI para bloqueio automático.

---

## 2) Artefatos entregues

- Política de versionamento:
  - `API_VERSIONING_POLICY.md`
- Baseline de compatibilidade:
  - `contracts/api_compatibility_baseline.json`
- Script de verificação:
  - `scripts/check_api_breaking_changes.py`
- Pipeline atualizado:
  - `.github/workflows/python-ci.yml` (job `api-compatibility-check`)

---

## 3) Regra de bloqueio implementada

A baseline atual considera breaking change:

- remoção de endpoint existente (`path + método`) em serviços da major ativa.

Comportamento:

- Se houver endpoint removido em relação ao baseline, o job falha.
- Mudanças aditivas (novos endpoints) não causam falha.

---

## 4) Validação executada

### Check de compatibilidade

- Execução local de `scripts/check_api_breaking_changes.py` com resultado **passed**.

### Regressão funcional

- `auth-service`: 13 passed
- `patient-service`: 13 passed
- `gateway-service`: 5 passed

---

## 5) Critérios de aceite da issue

- [x] Política publicada.
- [x] Breaking changes bloqueadas em CI.

Conclusão: ARC-03 tecnicamente concluída e pronta para encerramento da issue.
