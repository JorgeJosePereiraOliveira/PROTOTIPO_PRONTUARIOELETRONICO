# CLN-02 - Plano Executavel (Integracao CID/CIAP/SIGTAP)

- **Data de abertura:** 2026-03-11
- **Issue alvo:** #12 CLN-02 Integracao CID/CIAP/SIGTAP
- **Objetivo:** habilitar validacao semantica de codigos clinicos (CID, CIAP e SIGTAP) no contexto EMR, com testes e evidencias de qualidade para evolucao segura do prototipo.

---

## 1) Contexto e justificativa

Com CLN-01 concluida, a completude/coerencia SOAP foi fortalecida. O proximo passo natural e elevar a qualidade semantica dos dados clinicos, validando codigos de terminologias padronizadas antes da persistencia.

Esta entrega prepara a base para:
- padronizacao de classificacao clinica;
- rastreabilidade de codificacao;
- reducao de ambiguidade para analise longitudinal (CLN-03).

---

## 2) Escopo minimo vertical (primeira fase)

1. Implementar caso de uso de validacao de codigo terminologico no `emr-service`.
2. Suportar sistemas iniciais: `cid`, `ciap`, `sigtap`.
3. Validar formato de codigo por sistema.
4. Validar existencia/estado em catalogo inicial local (mock controlado).
5. Expor endpoint de validacao:
   - `GET /api/v1/emr/terminology/validate?system=...&code=...`
6. Cobrir com testes de API e contrato OpenAPI.

---

## 3) Regras iniciais de validacao

- `system` deve ser um de: `cid`, `ciap`, `sigtap`.
- Formatos iniciais:
  - `cid`: `A00`, `J45.9` (padrao CID-10 simplificado)
  - `ciap`: `A01` (letra + 2 digitos)
  - `sigtap`: 10 digitos numericos
- Codigo fora do padrao ou inexistente no catalogo inicial -> erro funcional.
- Resposta valida deve retornar: `system`, `code`, `status`, `description`, `valid`.

---

## 4) Sequencia executavel

1. Criar use case `validate_terminology_code_usecase.py`.
2. Integrar endpoint de validacao no `main.py` do EMR.
3. Adicionar testes de sucesso e erro no `test_emr_api.py`.
4. Atualizar teste de contrato OpenAPI para novo path.
5. Rodar testes do `emr-service`.
6. Publicar commit da primeira fatia da CLN-02.

---

## 5) Criterios de aceite da fase inicial

- [x] Endpoint de validacao de terminologia publicado.
- [x] Validacao de formato por sistema implementada.
- [x] Validacao de existencia em catalogo inicial implementada.
- [x] Testes de API cobrindo sucesso e falha.
- [x] Teste OpenAPI cobrindo novo path.
- [x] Execucao local do `emr-service` em verde.

---

## 6) Entregaveis esperados nesta fase

- Atualizacoes em `services/emr-service/src/emr/application/emr/`.
- Atualizacoes em `services/emr-service/src/emr/infra/api/main.py`.
- Atualizacoes em `services/emr-service/tests/test_emr_api.py`.
- Atualizacoes em `services/emr-service/tests/test_openapi_contract.py`.

---

## 7) Evidencia de encerramento da fase

- commit da fatia;
- resultado dos testes do `emr-service`;
- comentario na issue #12 com evidencias.

---

## 8) Segunda fase (logs de validacao terminologica)

1. Integrar emissao de evento de auditoria na criacao de problema clinico.
2. Registrar status `success` e `failed` para validacao terminologica.
3. Incluir `terminology_system` e `terminology_code` em metadata do evento.
4. Garantir que indisponibilidade do audit-service nao bloqueie fluxo clinico.
5. Cobrir com testes API e E2E.

Status da segunda fase:
- [x] Emissao de evento no `CreateProblem` (sucesso e falha).
- [x] Metadata de codificacao clinica registrada no evento.
- [x] Testes de API e E2E validados em verde.
