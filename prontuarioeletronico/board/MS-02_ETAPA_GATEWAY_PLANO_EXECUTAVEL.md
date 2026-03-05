# MS-02 — Etapa Gateway e Integração (Plano Executável)

- **Data de planejamento:** 2026-03-05
- **História relacionada:** US-2.2 Implementar Patient Service (fechamento integrado)
- **Objetivo desta etapa:** validar o `patient-service` no fluxo integrado por borda (API Gateway), com segurança JWT/RBAC propagada e testes de integração automatizados em pipeline.

---

## 1) Escopo da etapa (o que será implementado)

1. Introduzir camada de roteamento de borda (Gateway) para os serviços já ativos:
   - `auth-service`
   - `patient-service`
2. Publicar contratos de rota no gateway para:
   - login e fluxos de auth
   - CRUD de pacientes
3. Garantir propagação de cabeçalho `Authorization` do gateway para serviços internos.
4. Implementar suíte de testes de integração via gateway cobrindo:
   - autenticação real
   - autorização por perfil
   - token inválido/ausente
   - CRUD principal de pacientes
5. Integrar a suíte gateway no CI.

---

## 2) Princípios de escopo (coerência e precisão)

- Não reimplementar lógica de negócio no gateway.
- Gateway atua como camada de roteamento/orquestração HTTP.
- Reuso dos contratos já aprovados de `auth-service` e `patient-service`.
- Mudanças mínimas e rastreáveis para fechamento da US-2.2 em ambiente integrado.

---

## 3) Entregáveis técnicos previstos

### 3.1 Código

- `services/gateway-service/README.md`
- `services/gateway-service/requirements.txt`
- `services/gateway-service/src/gateway/infra/api/main.py`
- `services/gateway-service/tests/test_gateway_integration.py`
- `services/gateway-service/tests/test_gateway_openapi_contract.py`

### 3.2 Pipeline

- `.github/workflows/python-ci.yml`
  - novo job `gateway-integration-tests`

### 3.3 Documentação

- atualização deste plano com status de conclusão
- relatório de evidências da etapa gateway

---

## 4) Contratos de rota alvo (gateway)

### Auth (proxy)
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/verify`
- `GET /api/v1/auth/authorize`

### Patient (proxy)
- `POST /api/v1/patients`
- `GET /api/v1/patients`
- `GET /api/v1/patients/{patient_id}`
- `PUT /api/v1/patients/{patient_id}`
- `DELETE /api/v1/patients/{patient_id}`

---

## 5) Estratégia de testes de integração

### 5.1 Cenários obrigatórios

1. **Login real via gateway**
   - recebe `access_token` e `refresh_token` válidos.
2. **CRUD de paciente via gateway com token válido**
   - create/get/list/update funcionais.
3. **RBAC real via gateway**
   - `profissional` bloqueado no delete (`403`).
   - `admin` autorizado no delete (`200`).
4. **Token inválido/ausente via gateway**
   - retorno de negação coerente (`401`).

### 5.2 Critérios de qualidade

- Sem mocks de autorização no fluxo E2E de gateway.
- Testes determinísticos e isoláveis por ambiente.
- Compatibilidade com execução local e CI.

---

## 6) Checklist de aceite (etapa gateway)

- [ ] Gateway criado no padrão do projeto.
- [ ] Rotas de auth e patient publicadas no gateway.
- [ ] Propagação de `Authorization` validada.
- [ ] Testes de integração via gateway aprovados.
- [ ] Testes de contrato OpenAPI do gateway aprovados.
- [ ] CI com job de integração do gateway configurado e verde.
- [ ] Documentação de evidências atualizada.

---

## 7) Sequência de execução sugerida

1. Scaffold do `gateway-service` (template ARC-02 adaptado para proxy).
2. Implementação das rotas proxy para auth/patient.
3. Implementação dos testes de integração por token real.
4. Implementação dos testes de contrato OpenAPI do gateway.
5. Integração da suíte no CI.
6. Consolidação de relatório de evidências para issue.

---

## 8) Riscos e mitigação

1. **Falha de conectividade entre serviços durante testes**
   - Mitigação: testes com clients in-process quando aplicável e configuração explícita de URLs.
2. **Divergência de contrato entre gateway e serviços internos**
   - Mitigação: testes de contrato e smoke por endpoint proxy.
3. **Aumento de tempo de pipeline**
   - Mitigação: separar job de integração e otimizar instalação de dependências.

---

## 9) Resultado esperado da etapa

Ao final desta etapa, o projeto terá evidência de operação integrada por borda (gateway) para os serviços de autenticação e paciente, concluindo o fechamento técnico da US-2.2 em nível de plataforma, e não apenas em testes isolados por serviço.
