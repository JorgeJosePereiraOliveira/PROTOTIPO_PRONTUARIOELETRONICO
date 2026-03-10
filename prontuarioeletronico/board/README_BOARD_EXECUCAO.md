# Board Executável — Jira / GitHub Projects

Este diretório contém o board operacional do backlog técnico em formato executável.

## Navegação rápida
- Checklist de entrada em operação (go-live): [CHECKLIST_GO_LIVE_BOARD.md](CHECKLIST_GO_LIVE_BOARD.md)
- Relatório final de fechamento da execução: [RELATORIO_FECHAMENTO_EXECUCAO_BOARD.md](RELATORIO_FECHAMENTO_EXECUCAO_BOARD.md)
- Artefatos arquiteturais da ARC-01:
  - [ADR-001-clean-architecture.md](ADR-001-clean-architecture.md)
  - [CONTEXT_MAP.md](CONTEXT_MAP.md)
  - [ARQUITETURA_BASELINE.md](ARQUITETURA_BASELINE.md)
- Entrega da ARC-02:
  - [ARC-02_TEMPLATE_MICROSSERVICO.md](ARC-02_TEMPLATE_MICROSSERVICO.md)
- Entrega da ARC-03:
  - [ARC-03_PLANO_EXECUTAVEL_VERSIONAMENTO_API.md](ARC-03_PLANO_EXECUTAVEL_VERSIONAMENTO_API.md)
  - [ARC-03_RELATORIO_TECNICO_VERSIONAMENTO_API.md](ARC-03_RELATORIO_TECNICO_VERSIONAMENTO_API.md)
- Entrega da MS-01:
  - [MS-01_RELATORIO_TECNICO_DETALHADO.md](MS-01_RELATORIO_TECNICO_DETALHADO.md)
- Evolução da MS-02 (integração por gateway):
  - [MS-02_ETAPA_GATEWAY_PLANO_EXECUTAVEL.md](MS-02_ETAPA_GATEWAY_PLANO_EXECUTAVEL.md)
  - [MS-02_ETAPA_GATEWAY_RELATORIO_ACOES_REALIZADAS.md](MS-02_ETAPA_GATEWAY_RELATORIO_ACOES_REALIZADAS.md)
- Entrega da SEC-01:
  - [SEC-01_PLANO_EXECUTAVEL_SEGREDOS_HARDENING.md](SEC-01_PLANO_EXECUTAVEL_SEGREDOS_HARDENING.md)
  - [SEC-01_RELATORIO_TECNICO_SEGREDOS_HARDENING.md](SEC-01_RELATORIO_TECNICO_SEGREDOS_HARDENING.md)
- Entrega da MS-03:
  - [MS-03_PLANO_EXECUTAVEL_EMR_SERVICE.md](MS-03_PLANO_EXECUTAVEL_EMR_SERVICE.md)
  - [MS-03_RELATORIO_TECNICO_EMR_SERVICE.md](MS-03_RELATORIO_TECNICO_EMR_SERVICE.md)

## Estado atual de CI (baseline)

- Baseline de referencia em `main`: commit `7a968c9b6add267a30610fbcaf8b85b83e59c43a`
- Run de referencia: `22853210684`
- URL: `https://github.com/JorgeJosePereiraOliveira/PROTOTIPO_PRONTUARIOELETRONICO/actions/runs/22853210684`
- Checks obrigatorios no baseline: `core-tests`, `auth-service-tests`, `patient-service-tests`, `emr-service-tests`, `gateway-integration-tests`, `api-compatibility-check`, `security-baseline`.

Observacao:
- Falhas historicas em runs antigos podem existir e foram mantidas para rastreabilidade.
- Para operacao corrente e encerramento de issue, considerar sempre o ultimo baseline verde em `main`.

## Arquivos
- `board_backlog_executavel.csv` → base única com:
  - épico
  - história
  - prioridade (P0/P1)
  - estimativa (SP)
  - sprint alvo
  - dependências
  - responsável sugerido
  - critério de aceite
- `board_backlog_github_projects.csv` -> versão **normalizada para importação no GitHub Projects (VS Code + GitHub)** com colunas compatíveis: `Title`, `Body`, `Status`, `Labels`, `Repository`.
- `board_backlog_github_issues_ready.csv` -> versão para **importação de Issues** com colunas: `Title`, `Body`, `Labels`, `Assignees`, `Milestone`, `Repository`.

---

## 1) Como usar no GitHub Projects

1. Criar um Project (Table) no repositório/organização.
2. Importar CSV usando `board_backlog_github_projects.csv`.
3. O campo `Repository` já está configurado para `JorgeJosePereiraOliveira/PROTOTIPO_PRONTUARIOELETRONICO`.
4. Importar em modo draft item ou issue (conforme configuração do projeto).
5. Criar automações de status:
   - Todo -> In Progress -> Done

Observação: SP, dependências e responsável sugerido já estão descritos no `Body` de cada item e também em labels (`sp:*`, `priority:*`, `sprint:*`, `epic:*`).

Para criação prévia de Issues (antes de sincronizar com o Projects), utilize `board_backlog_github_issues_ready.csv`.

---

## 2) Como usar no Jira

1. Criar projeto Scrum (Company-managed).
2. Importar CSV (`System > External system import > CSV`).
3. Mapear campos:
   - `Story` -> Summary
   - `Descricao` -> Description
   - `Epic` -> Epic Name / Epic Link
   - `Prioridade` -> Priority
   - `SP` -> Story Points
   - `Status` -> Status
   - `Responsavel_Sugerido` -> Assignee
   - `Sprint` -> Sprint
   - `Dependencias` -> campo custom text (Dependencies)
4. Após import, criar issue links reais (`blocks/is blocked by`) com base no campo `Dependencias`.

---

## 3) Convenções de execução

- Priorização:
  - P0 = obrigatório para metas centrais do artigo.
  - P1 = consolidação técnica e evidências.
- Estimativa:
  - Fibonacci (3, 5, 8, 13).
- Definition of Done:
  - código + testes + CI verde + critérios de aceite + documentação atualizada.

---

## 4) Responsáveis sugeridos

Os nomes no CSV são **sugestões de papel** (ex.: DevOps 1, SRE 1, ML 1, DPO).
Na importação, substitua pelos usuários reais (GitHub/Jira) da equipe.

---

## 5) Recomendação prática

- Rodar planning por sprint com foco em:
  - dependências críticas liberadas primeiro;
  - capacidade por squad/papel;
  - risco regulatório (LGPD) e risco operacional (Kubernetes/segurança).

---

## 6) Evidência de conclusão da ARC-01

Para encerramento técnico da issue #1 (ARC-01), utilizar como evidência mínima:

- ADR aprovado: `ADR-001-clean-architecture.md`
- Mapa de contexto publicado: `CONTEXT_MAP.md`
- Baseline e checklist de conformidade: `ARQUITETURA_BASELINE.md`

---

## 7) Evidência de conclusão da ARC-02

Para encerramento técnico da ARC-02, utilizar como evidência mínima:

- Entrega formal da issue: `ARC-02_TEMPLATE_MICROSSERVICO.md`
- Gerador de serviço: `templates/create_microservice.py`
- Guia de uso e convenções: `templates/README_TEMPLATE_MICROSSERVICO.md`

---

## 8) Evidência de conclusão da MS-01 (Auth Service)

Para encerramento técnico da MS-01 / US-2.1, utilizar como evidência mínima:

- Relatório técnico consolidado: `MS-01_RELATORIO_TECNICO_DETALHADO.md`
- Código do serviço: `../services/auth-service/`
- Contrato OpenAPI validado: `../services/auth-service/tests/test_openapi_contract.py`
- Pipeline com execução do serviço: `../../.github/workflows/python-ci.yml`

---

## 9) Planejamento e rastreabilidade da etapa Gateway (MS-02)

Para execução da etapa integrada por borda (gateway), utilizar:

- Plano executável: `MS-02_ETAPA_GATEWAY_PLANO_EXECUTAVEL.md`
- Relatório de ações realizadas na preparação: `MS-02_ETAPA_GATEWAY_RELATORIO_ACOES_REALIZADAS.md`

---

## 10) Texto padrão de critério de aceite (proximas issues)

Utilizar o texto abaixo no fechamento tecnico de novas issues:

"Para aceite formal desta issue, considera-se o ultimo commit em `main` com checks obrigatorios em status `success` (baseline de estabilidade), alem do cumprimento dos criterios funcionais e documentais definidos no plano executavel da entrega. Runs historicos com falha sao preservados exclusivamente para rastreabilidade da evolucao tecnica do projeto."
