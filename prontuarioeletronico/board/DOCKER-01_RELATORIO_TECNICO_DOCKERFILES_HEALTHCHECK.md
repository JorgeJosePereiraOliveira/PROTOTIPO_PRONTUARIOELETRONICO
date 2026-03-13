# DOCKER-01 - Relatorio Tecnico (Dockerfiles com usuario nao-root e healthcheck)

- **Data de fechamento tecnico:** 2026-03-13
- **Issue alvo:** #15 DOCKER-01 Dockerfile por servico com usuario nao-root
- **Objetivo:** padronizar Dockerfiles dos microsservicos para build seguro e validacao de saude em runtime.

---

## 1) Escopo executado

1. Padronizacao de Dockerfile nos servicos:
   - `auth-service`
   - `patient-service`
   - `emr-service`
   - `scheduling-service`
   - `audit-service`
   - `professional-service`
   - `gateway-service`
2. Adocao de execucao em usuario nao-root (`appuser`) em todas as imagens.
3. Inclusao de `HEALTHCHECK` HTTP em `/health` em todas as imagens.
4. Build local de todas as imagens com tag de validacao `docker01`.
5. Validacao de subida de container e status `healthy` em runtime para todos os servicos.

---

## 2) Mudancas tecnicas realizadas

### 2.1 Dockerfiles padronizados

Arquivos atualizados:
- `services/auth-service/Dockerfile`
- `services/patient-service/Dockerfile`
- `services/emr-service/Dockerfile`
- `services/scheduling-service/Dockerfile`
- `services/audit-service/Dockerfile`
- `services/professional-service/Dockerfile`
- `services/gateway-service/Dockerfile`

Padrao aplicado:
- base image: `python:3.11-slim-bookworm`
- criacao de usuario dedicado:
  - `useradd --create-home --shell /usr/sbin/nologin appuser`
  - `chown -R appuser:appuser /app`
  - `USER appuser`
- healthcheck:
  - `HEALTHCHECK ... CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"`

Observacao especifica:
- `auth-service` recebeu `ENV AUTH_JWT_SECRET=change-me-dev-secret` para viabilizar subida containerizada em ambiente de desenvolvimento durante o teste de runtime da fatia.

---

## 3) Evidencias de validacao

### 3.1 Build das imagens

Comando executado (sequencial para os 7 servicos):
- `docker build -t tcc/<service>:docker01 ./services/<service>`

Resultado:
- **7/7 imagens buildadas com sucesso**.

### 3.2 Verificacao de requisitos por imagem

Validacao por inspeção (`docker image inspect`):
- `Config.User` = `appuser` em todas as imagens.
- `Config.Healthcheck.Test` presente em todas as imagens.

Resultado:
- **requisitos de usuario nao-root e healthcheck atendidos em 7/7**.

### 3.3 Validacao de runtime (sobe com healthcheck)

Execucao de containers para cada imagem e espera por status de saude:
- `docker run -d --name docker01-<service> tcc/<service>:docker01`
- polling de `docker inspect ... .State.Health.Status` ate `healthy`.

Resultado final:
- `docker01-auth-service` -> healthy
- `docker01-patient-service` -> healthy
- `docker01-emr-service` -> healthy
- `docker01-scheduling-service` -> healthy
- `docker01-audit-service` -> healthy
- `docker01-professional-service` -> healthy
- `docker01-gateway-service` -> healthy

Resultado consolidado:
- **7/7 containers sobem e atingem status healthy**.

---

## 4) Criterios de aceite (resultado)

- [x] Dockerfile por servico padronizado.
- [x] Execucao com usuario nao-root em todos os servicos.
- [x] Healthcheck configurado em todos os servicos.
- [x] Imagens buildam sem falha (7/7).
- [x] Containers sobem e ficam `healthy` (7/7).

---

## 5) Conclusao

A fatia executada de DOCKER-01 cumpriu o objetivo de endurecimento basico de conteinerizacao, estabelecendo padrao unico de Dockerfile para os servicos, reduzindo risco operacional por execucao privilegiada e adicionando verificacao nativa de saude para uso em compose/orquestracao e pipelines.
