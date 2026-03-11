# CLN-03 - Plano Executavel (Historico longitudinal por problema)

- **Data de abertura:** 2026-03-11
- **Issue alvo:** #13 CLN-03 Historico longitudinal por problema
- **Objetivo:** disponibilizar linha do tempo clinica por paciente/problema, consolidando evolucao do problema e registros SOAP em ordem cronologica.

---

## 1) Contexto e justificativa

Com CLN-02 concluida, a codificacao clinica passou a ser validada e auditada. O proximo passo e consolidar visao longitudinal por problema, requisito essencial para acompanhamento clinico continuo e analise evolutiva.

---

## 2) Escopo da primeira fatia (vertical)

1. Introduzir referencia temporal (`created_at`) para problema e SOAP no EMR.
2. Implementar use case de timeline por paciente com filtro opcional por problema.
3. Expor endpoint:
   - `GET /api/v1/emr/timeline?patient_id=...&problem_id=...`
4. Integrar rota correspondente no gateway.
5. Cobrir com testes no `emr-service` e `gateway-service`.
6. Atualizar documentacao do board com plano da CLN-03.

---

## 3) Regras da fatia inicial

- `patient_id` obrigatorio.
- `problem_id` opcional para refino da linha do tempo.
- Quando `problem_id` informado e inexistente para o paciente, retornar erro funcional (`problem not found`).
- Timeline deve retornar eventos em ordem cronologica crescente.
- Eventos iniciais cobertos:
  - `problem` (abertura/evolucao do problema)
  - `soap` (evolucoes clinicas SOAP vinculadas ao problema)

---

## 4) Criterios de aceite da fatia

- [x] Endpoint de timeline publicado no EMR.
- [x] Proxy de timeline publicado no gateway.
- [x] Linha do tempo retornando eventos de problema e SOAP ordenados.
- [x] Cobertura de testes de API e integracao para timeline.
- [x] Execucao local de suites relevantes em verde.
- [x] Evidencia publicada na issue #13.

---

## 5) Evidencia esperada de encerramento da fatia

- commit com mudancas tecnicas da timeline;
- resultados de teste em verde (`emr-service` e integracao gateway);
- comentario na issue #13 com escopo e evidencias.
