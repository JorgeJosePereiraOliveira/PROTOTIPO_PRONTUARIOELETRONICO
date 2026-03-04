# Checklist Go-Live do Board (GitHub Issues + GitHub Projects)

Este checklist operacionaliza o backlog documentado em `board/` para início de execução com consistência e produtividade.

---

## 1) Pré-Go-Live (preparação de dados)

- [ ] Confirmar que os arquivos-base estão atualizados:
  - [ ] `board_backlog_executavel.csv`
  - [ ] `board_backlog_github_projects.csv`
  - [ ] `board_backlog_github_issues_ready.csv`
- [ ] Validar slug do repositório em todos os CSVs:
  - [ ] `JorgeJosePereiraOliveira/PROTOTIPO_PRONTUARIOELETRONICO`
- [ ] Revisar encoding UTF-8 e delimitador de colunas.
- [ ] Conferir se todos os itens possuem:
  - [ ] `Title`
  - [ ] `Labels`
  - [ ] `Milestone`
  - [ ] `Assignees` (ou placeholder assumido)

---

## 2) Preparação do repositório GitHub

- [ ] Criar labels padrão (se ainda não existirem):
  - [ ] `priority:p0`, `priority:p1`
  - [ ] `epic:*` (plataforma-base, microservicos, cicd, kubernetes, etc.)
  - [ ] `sprint:1` ... `sprint:8`
  - [ ] `sp:3`, `sp:5`, `sp:8`, `sp:13`
- [ ] Criar milestones:
  - [ ] `Sprint 1`
  - [ ] `Sprint 2`
  - [ ] `Sprint 3`
  - [ ] `Sprint 4`
  - [ ] `Sprint 5`
  - [ ] `Sprint 6`
  - [ ] `Sprint 7`
  - [ ] `Sprint 8`
- [ ] Definir datas de início/fim em cada milestone.
- [ ] Validar permissões da equipe para criação/edição de Issues e Projects.

---

## 3) Importação de Issues (fonte operacional)

- [ ] Substituir placeholders de assignees por usernames GitHub reais no arquivo:
  - [ ] `board_backlog_github_issues_ready.csv`
- [ ] Importar o CSV de Issues no repositório.
- [ ] Verificar quantitativo pós-import:
  - [ ] Total de issues esperado = total de histórias no backlog
- [ ] Conferir amostragem de 5 issues:
  - [ ] Body completo
  - [ ] Labels corretas
  - [ ] Milestone correta
  - [ ] Assignee atribuído

---

## 4) Configuração do GitHub Projects (execução visual)

- [ ] Criar/abrir Project (Table) vinculado ao repositório.
- [ ] Adicionar campos (se necessário):
  - [ ] `Status`
  - [ ] `Priority`
  - [ ] `Iteration` (opcional)
  - [ ] `Estimate` (opcional, se decidir separar de labels)
- [ ] Sincronizar Issues importadas ao Project.
- [ ] Mapear fluxo de status:
  - [ ] `Todo`
  - [ ] `In Progress`
  - [ ] `Done`
- [ ] Criar visualizações mínimas:
  - [ ] Por Sprint
  - [ ] Por Epic
  - [ ] Por Responsável
  - [ ] Por Prioridade (P0/P1)

---

## 5) Dependências e governança

- [ ] Converter dependências textuais do Body em links explícitos entre issues (quando aplicável).
- [ ] Definir política de bloqueio:
  - [ ] Issue bloqueada não entra em `In Progress` sem desbloqueio.
- [ ] Publicar regra de priorização:
  - [ ] P0 sempre precede P1 quando houver conflito de capacidade.
- [ ] Definir cadência de rituais:
  - [ ] Planning semanal/quinzenal
  - [ ] Daily
  - [ ] Review
  - [ ] Retrospectiva

---

## 6) Sprint 0 (validação de processo)

- [ ] Selecionar 2 a 4 issues P0 para execução piloto.
- [ ] Rodar ciclo completo:
  - [ ] Todo -> In Progress -> Done
  - [ ] PR vinculado à issue
  - [ ] Critério de aceite verificado
- [ ] Validar métricas mínimas:
  - [ ] Lead time
  - [ ] Throughput
  - [ ] Bloqueios por dependência
- [ ] Ajustar board/processo com base no aprendizado do piloto.

---

## 7) Definition of Done (DoD) operacional

Uma issue só pode ir para `Done` quando:

- [ ] Critérios de aceite da história atendidos.
- [ ] Código revisado e mergeado.
- [ ] Testes automatizados relevantes passaram.
- [ ] CI verde.
- [ ] Documentação/README atualizados (quando aplicável).
- [ ] Evidências anexadas (prints/logs/links de PR/deploy).

---

## 8) Checklist de qualidade contínua do board

- [ ] Nenhuma issue sem prioridade.
- [ ] Nenhuma issue sem sprint/milestone.
- [ ] Nenhuma issue sem responsável (exceto backlog intencional).
- [ ] Nenhuma issue em `In Progress` sem PR vinculado.
- [ ] Nenhuma issue `Done` sem evidência de aceite.

---

## 9) Critério de Go-Live concluído

Considere o board oficialmente em produção quando:

- [ ] 100% das histórias importadas como Issues.
- [ ] 100% das issues com milestone e prioridade.
- [ ] >= 90% das issues com assignee real definido.
- [ ] Fluxo de status operacional e testado no Sprint 0.
- [ ] Time alinhado com cerimônias e DoD.

---

## 10) Referência rápida dos arquivos do board

- `board_backlog_executavel.csv` — base principal do backlog.
- `board_backlog_github_projects.csv` — importação para Project.
- `board_backlog_github_issues_ready.csv` — importação de Issues com assignee/milestone.
- `README_BOARD_EXECUCAO.md` — guia de uso Jira/GitHub.
- `CHECKLIST_GO_LIVE_BOARD.md` — este checklist de entrada em operação.
- `ADR-001-clean-architecture.md` — decisão arquitetural oficial (ARC-01).
- `CONTEXT_MAP.md` — mapa de contextos e integrações permitidas.
- `ARQUITETURA_BASELINE.md` — baseline e checklist de conformidade para PR.
