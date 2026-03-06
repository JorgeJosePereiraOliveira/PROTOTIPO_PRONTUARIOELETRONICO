# ARC-03 — Plano Executável (Versionamento de APIs e Breaking Changes)

- **Data de abertura:** 2026-03-06
- **Issue alvo:** #3 ARC-03 Padronizar versionamento de APIs e breaking changes
- **Objetivo:** publicar política de versionamento e bloquear breaking changes em CI.

---

## 1) Escopo

1. Publicar política oficial de versionamento de APIs REST.
2. Definir baseline de contrato por serviço (`auth`, `patient`, `gateway`).
3. Implementar verificador automático de compatibilidade (detecção de remoção de paths/métodos).
4. Integrar a verificação no pipeline CI para bloquear regressões de contrato.

---

## 2) Entregáveis

- Documento: `API_VERSIONING_POLICY.md`
- Baseline: `contracts/api_compatibility_baseline.json`
- Script de verificação: `scripts/check_api_breaking_changes.py`
- Job CI: atualização em `.github/workflows/python-ci.yml`
- Evidência técnica no board.

---

## 3) Critérios de aceite

- [ ] Política de versionamento publicada e referenciada na documentação.
- [ ] Breaking changes de contrato bloqueadas automaticamente no CI.
- [ ] Validação local do check com retorno verde no estado atual.

---

## 4) Estratégia de bloqueio de breaking changes

- Gerar visão atual de contratos a partir de `app.openapi()` dos serviços.
- Comparar com baseline versionada no repositório.
- Falhar quando houver remoção de endpoint existente (`path + método`).
- Permitir evolução aditiva (novos endpoints) sem falha.

---

## 5) Próximos passos após fechamento

- Aplicar versionamento semântico por serviço com changelog obrigatório por release.
- Evoluir verificação para cobertura de schemas (campos obrigatórios removidos) em próxima iteração.
