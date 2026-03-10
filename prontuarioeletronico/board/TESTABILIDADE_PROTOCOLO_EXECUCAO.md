# Protocolo de Testabilidade do Prototipo

## 1) Objetivo

Padronizar a evidencia de qualidade para cada entrega do backlog tecnico, garantindo rastreabilidade entre codigo, testes, pipeline e documentacao do board.

---

## 2) Matriz minima por entrega

Para cada issue tecnica (principalmente P0), registrar no relatorio:

1. **Teste de servico**
- comando executado
- resultado (pass/fail + contagem)

2. **Teste de borda/gateway** (quando aplicavel)
- comando executado
- resultado

3. **Compatibilidade de API**
- execucao de `scripts/check_api_breaking_changes.py`
- resultado

4. **Seguranca baseline**
- job `security-baseline` em `success`

5. **Run final em main**
- commit
- id do run
- URL do run
- status

---

## 3) Suites obrigatorias por contexto atual

### 3.1 Core e servicos existentes
- `prontuarioeletronico/services/auth-service/tests`
- `prontuarioeletronico/services/patient-service/tests`
- `prontuarioeletronico/services/emr-service/tests`
- `prontuarioeletronico/services/scheduling-service/tests`
- `prontuarioeletronico/services/gateway-service/tests`

### 3.2 Guardrails transversais
- `prontuarioeletronico/scripts/check_api_breaking_changes.py`
- workflow `.github/workflows/python-ci.yml`

---

## 4) Regra de aceite para documentacao

Uma issue so deve ser marcada como pronta para encerramento quando houver:
- plano executavel atualizado;
- relatorio tecnico com evidencias;
- comentario na issue com link do run final em `main`.

---

## 5) Checklist rapido por PR

- [ ] testes locais do servico executados
- [ ] testes de gateway executados (se aplicavel)
- [ ] checker de compatibilidade executado
- [ ] sem regressao nos checks obrigatorios
- [ ] evidencia adicionada no board e na issue GitHub
