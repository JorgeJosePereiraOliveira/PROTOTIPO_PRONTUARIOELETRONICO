# CLN-01 - Plano Executavel (Validacao de Completude SOAP)

- **Data de abertura:** 2026-03-10
- **Issue alvo:** #10 CLN-01 Validacao de completude SOAP
- **Objetivo:** reforcar regras de completude e coerencia clinica do registro SOAP no `emr-service`, bloqueando persistencia de registros incompletos/ambiguos e mantendo rastreabilidade em testes e CI.

---

## 1) Contexto e justificativa

Com a MS-03 concluida, o EMR ja possui operacoes SOAP por API. O proximo passo natural e aumentar a qualidade clinica dos dados, garantindo que os registros tenham completude minima e consistencia entre secoes (`subjective`, `objective`, `assessment`, `plan`).

A entrega CLN-01 foca em:
- reduzir ambiguidade de registro clinico;
- impedir persistencia de SOAP estruturalmente incompleto;
- preparar base para CLN-02 (terminologias clinicas) e CLN-03 (historico longitudinal).

---

## 2) Escopo minimo vertical (entrega desta issue)

1. Definir e implementar regras de validacao de completude SOAP no `CreateSOAPUseCase`.
2. Garantir mensagens de erro clinicas objetivas por campo/regra.
3. Manter compatibilidade da API existente (`POST /api/v1/emr/soap`) sem breaking change de contrato.
4. Cobrir regras com testes unitarios e de API no `emr-service`.
5. Validar impacto no gateway (fluxo proxy inalterado para chamadas validas/invalidas).
6. Atualizar documentacao tecnica da entrega (plano + relatorio CLN-01).

---

## 3) Regras clinicas iniciais de validacao (MVP)

### 3.1 Regras de completude por secao
- `subjective`: obrigatorio, minimo de 10 caracteres uteis.
- `objective`: obrigatorio, minimo de 10 caracteres uteis.
- `assessment`: obrigatorio, minimo de 10 caracteres uteis.
- `plan`: obrigatorio, minimo de 10 caracteres uteis.

### 3.2 Regras de coerencia basica
- Nao permitir registros com secoes repetidas literalmente (ex.: `assessment == plan`).
- Nao permitir texto placeholder em campos clinicos (`"n/a"`, `"na"`, `"-"`, `"."`, `"sem dados"`).
- Manter vinculo consistente com `problem_id` existente (regra ja presente, deve permanecer obrigatoria).

### 3.3 Erros funcionais esperados
- Violacao de completude/coerencia -> `400` com `detail` explicito da regra violada.
- `problem_id` inexistente -> `404` (`problem not found`).

---

## 4) Arquivos alvo para inicio imediato da implementacao

Implementacao principal:
- `services/emr-service/src/emr/application/emr/create_soap_usecase.py`

Apoio (se necessario para separar regras):
- `services/emr-service/src/emr/application/emr/soap_validation_rules.py`

API e mapeamento de erros:
- `services/emr-service/src/emr/infra/api/main.py`

Testes (obrigatorios nesta issue):
- `services/emr-service/tests/test_emr_api.py`
- `services/emr-service/tests/test_authorization_e2e.py` (somente se houver impacto)
- `services/emr-service/tests/test_openapi_contract.py` (garantir que contrato permanece valido)

Gateway (checagem de nao regressao):
- `services/gateway-service/tests/test_gateway_integration.py`

---

## 5) Sequencia executavel (passo a passo)

1. Mapear estado atual das validacoes SOAP em `create_soap_usecase.py`.
2. Implementar regras de completude e coerencia do MVP CLN-01.
3. Padronizar mensagens de erro por regra violada.
4. Ajustar camada API para manter semantica HTTP (`400` validacao, `404` problema inexistente).
5. Criar testes novos para cada regra de validacao e cenarios de sucesso.
6. Rodar `pytest -q tests` no `emr-service`.
7. Rodar `pytest -q tests` no `gateway-service` para nao regressao.
8. Rodar `python scripts/check_api_breaking_changes.py` no diretorio `prontuarioeletronico`.
9. Atualizar relatorio tecnico CLN-01 com evidencias de execucao.
10. Publicar commit/PR com checklist de aceite preenchido.

---

## 6) Criterios de aceite da CLN-01

- [ ] Regras de completude SOAP implementadas e ativas em runtime.
- [ ] Regras de coerencia basica implementadas.
- [ ] Mensagens de erro clinicas claras para cada violacao.
- [ ] Fluxo de persistencia bloqueia SOAP invalido.
- [ ] Testes do `emr-service` cobrindo cenarios validos e invalidos.
- [ ] Nao regressao no gateway e na compatibilidade de API.
- [ ] Evidencia de run verde em `main` para aceite formal.

---

## 7) Entregaveis esperados

- Regras de validacao SOAP implementadas no `emr-service`.
- Testes automatizados de completude/coerencia SOAP.
- Relatorio tecnico de fechamento:
  - `board/CLN-01_RELATORIO_TECNICO_VALIDACAO_COMPLETUDE_SOAP.md`.
- Atualizacao de rastreabilidade no board (indice + referencia de baseline, se aplicavel).

---

## 8) Riscos e mitigacoes

1. **Regra clinica excessivamente restritiva**
- Mitigacao: iniciar com MVP de coerencia basica e evoluir por feedback clinico.

2. **Mudanca comportamental sem cobertura suficiente**
- Mitigacao: testes dedicados por regra + teste de nao regressao no gateway.

3. **Inconsistencia de mensagens de erro**
- Mitigacao: padrao unico de mensagens no use case e asserts explicitos nos testes.

---

## 9) Evidencia de encerramento (template)

No fechamento tecnico da issue CLN-01, registrar:
- links dos commits principais;
- link do run baseline em `main` com checks obrigatorios em `success`;
- resumo objetivo dos testes executados (emr + gateway + compatibilidade);
- referencias para plano e relatorio tecnico da CLN-01.
