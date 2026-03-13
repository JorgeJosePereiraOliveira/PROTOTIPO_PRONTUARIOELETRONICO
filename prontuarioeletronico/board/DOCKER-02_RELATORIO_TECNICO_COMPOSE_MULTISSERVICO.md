# DOCKER-02 - Relatorio Tecnico (Compose multi-servico)

- **Data de fechamento tecnico:** 2026-03-13
- **Issue alvo:** #16 DOCKER-02 Compose para stack local integrada
- **Objetivo:** disponibilizar composicao local unica para subir gateway e microsservicos com dependencias e verificacao de saude.

---

## 1) Escopo executado

1. Criacao do arquivo de orquestracao local:
   - `services/docker-compose.microservices.yml`
2. Inclusao dos servicos na stack:
   - `auth-service`
   - `patient-service`
   - `emr-service`
   - `scheduling-service`
   - `audit-service`
   - `professional-service`
   - `gateway-service`
3. Configuracao de rede interna por nome de servico (`<service>:8000`).
4. Configuracao de variaveis de ambiente de integracao entre servicos.
5. Definicao de persistencia SQLite por volumes nomeados para os 6 servicos com banco local.
6. Definicao de dependencia com `depends_on` + `condition: service_healthy` para ordem de subida.

---

## 2) Mudancas tecnicas realizadas

### 2.1 Arquivo compose multi-servico

Arquivo criado:
- `services/docker-compose.microservices.yml`

Elementos principais do compose:
- imagens/tag de validacao: `tcc/<service>:docker02`
- mapeamento de portas:
  - gateway `8000:8000`
  - auth `8001:8000`
  - patient `8002:8000`
  - emr `8003:8000`
  - scheduling `8004:8000`
  - audit `8005:8000`
  - professional `8006:8000`
- healthcheck HTTP por servico em `/health`
- volumes nomeados para dados SQLite:
  - `auth_data`, `patient_data`, `emr_data`, `scheduling_data`, `audit_data`, `professional_data`

### 2.2 Ajuste de permissao para persistencia SQLite com usuario nao-root

Durante validacao inicial, o `auth-service` falhou com:
- `sqlite3.OperationalError: unable to open database file`

Acao corretiva aplicada:
1. Padronizacao de path de banco no compose para `sqlite:////app/data/<service>.db`.
2. Garantia de existencia do diretorio de dados na imagem e ownership do `appuser`:
   - Dockerfiles atualizados em:
     - `services/auth-service/Dockerfile`
     - `services/patient-service/Dockerfile`
     - `services/emr-service/Dockerfile`
     - `services/scheduling-service/Dockerfile`
     - `services/audit-service/Dockerfile`
     - `services/professional-service/Dockerfile`
   - ajuste aplicado no build stage:
     - `mkdir -p /app/data`
     - `chown -R appuser:appuser /app`

Resultado: escrita SQLite funcional mantendo execucao non-root.

---

## 3) Evidencias de validacao

### 3.1 Validacao sintatica do compose

Comando:
- `docker compose -f services/docker-compose.microservices.yml config --quiet`

Resultado:
- sem erros de configuracao.

### 3.2 Subida da stack com build

Comando:
- `docker compose -f services/docker-compose.microservices.yml up -d --build`

Resultado final apos ajuste de permissao:
- **7/7 servicos iniciados e em estado healthy**.

### 3.3 Verificacao de status dos containers

Comando:
- `docker compose -f services/docker-compose.microservices.yml ps`

Resultado:
- `tcc-auth-service` -> Up (healthy)
- `tcc-patient-service` -> Up (healthy)
- `tcc-emr-service` -> Up (healthy)
- `tcc-scheduling-service` -> Up (healthy)
- `tcc-audit-service` -> Up (healthy)
- `tcc-professional-service` -> Up (healthy)
- `tcc-gateway-service` -> Up (healthy)

### 3.4 Smoke test de borda (gateway)

Comando:
- `curl http://localhost:8000/health`

Resposta:
- `{"status":"healthy","service":"gateway"}`

---

## 4) Criterios de aceite (resultado)

- [x] Compose local multi-servico criado para stack integrada.
- [x] Gateway e microsservicos sobem por um unico comando.
- [x] Dependencias entre servicos respeitam estado de saude (`service_healthy`).
- [x] Persistencia SQLite com volumes nomeados funcional em execucao non-root.
- [x] Stack operacional validada com healthchecks e smoke test do gateway.

---

## 5) Conclusao

A entrega DOCKER-02 foi concluida com sucesso, disponibilizando uma stack local integrada, reproduzivel e validada para desenvolvimento e demonstracao do prototipo. A composicao reduz atrito operacional para execucao ponta a ponta e prepara base para etapas seguintes de observabilidade, automacao e endurecimento de ambiente.