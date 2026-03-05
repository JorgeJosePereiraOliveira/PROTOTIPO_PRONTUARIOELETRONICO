# MS-02 — Plano Executável (Patient Service)

- **Data de abertura:** 2026-03-05
- **Story alvo:** US-2.2 Implementar Patient Service
- **Objetivo:** entregar CRUD de paciente com contrato OpenAPI, segurança JWT/RBAC e validação em CI.

## 1) Escopo da primeira implementação

1. Criar `patient-service` a partir do template ARC-02.
2. Implementar domínio de paciente (entidade + contrato de repositório).
3. Implementar casos de uso mínimos:
   - criar paciente
   - buscar paciente por id
   - listar pacientes
4. Expor endpoints REST versionados (`/api/v1/patients`).
5. Adicionar testes automatizados:
   - API funcional
   - contrato OpenAPI mínimo
6. Integrar suíte do `patient-service` no pipeline CI.

## 2) Arquivos previstos (fase 1)

### Serviço
- `services/patient-service/README.md`
- `services/patient-service/requirements.txt`
- `services/patient-service/src/patient/domain/patient/`
- `services/patient-service/src/patient/application/patient/`
- `services/patient-service/src/patient/infra/patient/`
- `services/patient-service/src/patient/infra/api/main.py`

### Testes
- `services/patient-service/tests/test_patient_api.py`
- `services/patient-service/tests/test_openapi_contract.py`

### Governança/CI
- `.github/workflows/python-ci.yml`

## 3) Endpoints alvo (fase 1)

- `GET /health`
- `GET /api/v1/info`
- `POST /api/v1/patients`
- `GET /api/v1/patients/{patient_id}`
- `GET /api/v1/patients`

## 4) Estratégia de testes

1. **Teste funcional API**
   - criação de paciente retorna `201`
   - consulta por id retorna `200` ou `404`
   - listagem retorna coleção
2. **Teste de contrato OpenAPI**
   - paths obrigatórios presentes
   - schema de request/response de paciente presente
3. **Execução local**
   - `pytest -q services/patient-service/tests`

## 5) Checklist de aceite (MS-02 parcial — fase 1)

- [x] Serviço inicial criado no padrão ARC-02.
- [x] Endpoints de paciente fase 1 implementados.
- [x] Testes de API passando.
- [x] Testes de contrato OpenAPI passando.
- [x] CI com job do `patient-service` configurado.
- [x] README do serviço atualizado com execução e endpoints.

## 6) Próxima fase (fase 2)

- adicionar update/delete
- aplicar autenticação/autorizações por papel
- persistência SQLAlchemy
- integração com auth-service (token real)
