# Board Executável — Jira / GitHub Projects

Este diretório contém o board operacional do backlog técnico em formato executável.

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

---

## 1) Como usar no GitHub Projects

1. Criar um Project (Table) no repositório/organização.
2. Importar CSV usando `board_backlog_executavel.csv`.
3. Mapear colunas:
   - `Story` -> Title
   - `Descricao` -> Description
   - `Status` -> Status
   - `Prioridade` -> Priority (single select)
   - `SP` -> Estimate (number)
   - `Sprint` -> Iteration
   - `Responsavel_Sugerido` -> Assignee
   - `Epic` -> Label (ou campo custom)
   - `Dependencias` -> campo texto "Depends on"
4. Criar labels para cada `Epic`.
5. Criar automações de status:
   - Todo -> In Progress -> Done

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
