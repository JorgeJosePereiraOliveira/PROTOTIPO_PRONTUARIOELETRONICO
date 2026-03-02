# README Backlog Técnico Priorizado

## 1) Objetivo deste documento

Este documento consolida o **Backlog Técnico Priorizado** do projeto **prontuarioeletronico**, alinhado ao artigo:

**"Conteinerização e Orquestração de Microsserviços para Prontuário Eletrônico Baseado em RCOP e Inteligência Artificial"**.

O foco é orientar a execução em sprints com aderência a:
- Princípios de **Arquitetura Limpa**;
- Decomposição em **microsserviços**;
- **Conteinerização** com Docker;
- **Orquestração** com Kubernetes;
- Pipeline **CI/CD**;
- Práticas de **MLOps**;
- Requisitos de **segurança e LGPD**.

---

## 2) Premissas arquiteturais (obrigatórias)

1. **Regra da Dependência (Clean Architecture)**
   - Dependências apontam para dentro (Infra -> Application -> Domain).
   - Regras de negócio não dependem de framework, banco ou detalhes de transporte.

2. **Bounded contexts e baixo acoplamento**
   - Serviços independentes por domínio: Auth, Patient, EMR, Scheduling, Audit, AI.
   - Compartilhamento apenas via contratos/API/eventos, nunca acesso direto ao banco de outro serviço.

3. **Segurança e privacidade by design**
   - Princípio do menor privilégio.
   - Dados sensíveis com proteção em trânsito e em repouso.
   - Trilha de auditoria para operações críticas.

4. **Operabilidade cloud-native**
   - Serviços observáveis (logs, métricas, tracing).
   - Deploy reproduzível e rollback seguro.

---

## 3) Priorização e estratégia

### Níveis
- **P0 (Crítico)**: bloqueia objetivos centrais do artigo.
- **P1 (Alto)**: necessário para robustez e publicação de resultados consistentes.
- **P2 (Médio)**: melhorias evolutivas e otimizações.

### Estratégia de entrega
- Entregar primeiro a espinha dorsal técnica (arquitetura, serviços principais, segurança, deploy e pipeline).
- Em seguida, consolidar observabilidade, AI/MLOps e métricas experimentais para resultados científicos.

---

## 4) Backlog por épico

## Épico 1 — Plataforma Base e Governança Arquitetural (P0)

### US-1.1 Definir contratos de arquitetura e fronteiras de domínio
**Descrição**: formalizar bounded contexts, contratos de integração e regras de dependência.

**Critérios de aceite**:
- ADRs (Architecture Decision Records) publicados e versionados.
- Mapa de contextos do sistema aprovado.
- Checklist de revisão arquitetural sem violações de acoplamento.

### US-1.2 Padronizar template de microsserviço em Clean Architecture
**Descrição**: criar esqueleto reutilizável (domain/application/infra, testes, lint, docs).

**Critérios de aceite**:
- Template de serviço disponível no repositório.
- Novo serviço criado em < 30 min com testes mínimos passando.
- Convenções de pastas, naming e contratos documentadas.

### US-1.3 Política de versionamento e compatibilidade de APIs
**Descrição**: padronizar versionamento semântico e gestão de breaking changes.

**Critérios de aceite**:
- Política de versionamento publicada.
- Breaking change bloqueada por validação no pipeline.
- Changelog por serviço obrigatório.

---

## Épico 2 — Decomposição em Microsserviços (P0)

### US-2.1 Implementar Auth Service
**Descrição**: autenticação, autorização e perfis de acesso clínico.

**Critérios de aceite**:
- Emissão e validação de JWT funcionando.
- RBAC mínimo: admin, profissional de saúde.
- Endpoint de health/readiness e teste de carga básico.

### US-2.2 Implementar Patient Service
**Descrição**: gerenciamento de dados demográficos e cadastrais.

**Critérios de aceite**:
- CRUD completo de paciente com validações.
- Contrato OpenAPI publicado.
- Testes de contrato e integração com gateway aprovados.

### US-2.3 Implementar EMR Service e Scheduling Service
**Descrição**: núcleo clínico (RCOP/SOAP) e agendamento desacoplado.

**Critérios de aceite**:
- Operações RCOP/SOAP disponíveis por API.
- Agendamento independente do EMR.
- Nenhum serviço acessa banco de outro serviço.

### US-2.4 Implementar Audit Service
**Descrição**: rastreabilidade de eventos críticos.

**Critérios de aceite**:
- Eventos críticos persistidos com timestamp e ator.
- Consulta de auditoria por período/usuário/operação.
- Retenção e integridade de logs definidas.

---

## Épico 3 — Modelo Clínico RCOP/SOAP e Qualidade de Dados (P0)

### US-3.1 Validar completude e coerência SOAP
**Descrição**: impedir registros incompletos/ambíguos em campos críticos.

**Critérios de aceite**:
- Campos obrigatórios por etapa clínica validados.
- Regras de consistência entre seções SOAP implementadas.
- Mensagens de erro clínicas claras para o usuário.

### US-3.2 Integrar terminologias clínicas (CID, CIAP, SIGTAP)
**Descrição**: padronização semântica e suporte à codificação.

**Critérios de aceite**:
- Lookup de códigos com validação de formato/status.
- Código inválido bloqueia persistência.
- Logs de auditoria para codificação clínica.

### US-3.3 Histórico longitudinal por problema
**Descrição**: consolidar linha do tempo por problema clínico.

**Critérios de aceite**:
- Consulta cronológica por problema e paciente.
- Histórico inclui evolução SOAP e plano terapêutico.
- Performance de consulta dentro de SLO definido.

---

## Épico 4 — Segurança, Privacidade e LGPD (P0)

### US-4.1 Gestão de consentimento e base legal
**Descrição**: registrar base legal e consentimentos aplicáveis.

**Critérios de aceite**:
- Registro de consentimento versionado por paciente.
- Fluxo de revogação/atualização de consentimento.
- Evidências de minimização de dados por caso de uso.

### US-4.2 Proteção de dados sensíveis
**Descrição**: criptografia, segredos e controle de acesso.

**Critérios de aceite**:
- TLS obrigatório em tráfego externo/interno crítico.
- Segredos fora do código, com rotação documentada.
- Perfis RBAC aplicados e auditáveis.

### US-4.3 Direitos do titular (LGPD)
**Descrição**: operacionalizar acesso, retificação e eliminação/anonimização.

**Critérios de aceite**:
- Fluxos implementados e testados ponta a ponta.
- Trilha de auditoria de solicitações do titular.
- Política de retenção/expurgo documentada.

---

## Épico 5 — Conteinerização e Supply Chain (P0)

### US-5.1 Dockerfile por serviço com hardening
**Descrição**: imagens leves, não-root e builds reproduzíveis.

**Critérios de aceite**:
- Todos os serviços com Dockerfile próprio.
- Imagem executa com usuário não privilegiado.
- Healthcheck funcional por serviço.

### US-5.2 Ambiente local multi-serviço via Docker Compose
**Descrição**: experiência de desenvolvimento integrada.

**Critérios de aceite**:
- Subida local com gateway + serviços + bancos.
- Scripts de bootstrap e teardown documentados.
- Teste de integração executável localmente.

### US-5.3 Segurança de cadeia de suprimento
**Descrição**: scan de imagens e geração de SBOM.

**Critérios de aceite**:
- Vulnerabilidades críticas bloqueiam release.
- SBOM gerado e armazenado por build.
- Proveniência de imagem rastreável.

---

## Épico 6 — Orquestração Kubernetes (P0)

### US-6.1 Deploy base por serviço
**Descrição**: manifests Helm/Kustomize com Deployments/Services/Ingress.

**Critérios de aceite**:
- Deploy funcional em cluster de homologação.
- Readiness/liveness probes em todos os pods.
- Configuração por ambiente via ConfigMap/Secret.

### US-6.2 Escalabilidade e resiliência
**Descrição**: HPA e recuperação automática de falhas.

**Critérios de aceite**:
- HPA ativo para serviços críticos.
- Teste de falha comprova self-healing sem indisponibilidade perceptível.
- PDB/estratégia de atualização sem downtime.

### US-6.3 Operação segura em cluster
**Descrição**: limites, quotas e políticas de rede.

**Critérios de aceite**:
- Resource requests/limits definidos.
- NetworkPolicies restringindo tráfego lateral.
- Processo de rollback validado em homolog.

---

## Épico 7 — CI/CD (P0)

### US-7.1 Pipeline de qualidade contínua
**Descrição**: lint, testes, cobertura, segurança e build.

**Critérios de aceite**:
- PR só mergeia com checks obrigatórios verdes.
- Cobertura mínima por serviço estabelecida e monitorada.
- Testes de contrato e integração automatizados.

### US-7.2 Publicação e promoção de artefatos
**Descrição**: build versionado e publicação em registry.

**Critérios de aceite**:
- Imagem assinada/versionada por commit/tag.
- Promoção de artefatos dev -> homolog -> prod rastreável.
- Bloqueio automático para artefatos sem evidências de qualidade.

### US-7.3 Deploy contínuo com estratégia segura
**Descrição**: rollout progressivo e rollback automático.

**Critérios de aceite**:
- Canary ou blue/green disponível para serviços críticos.
- Rollback por falha de SLO automatizado.
- Evidência de deployment auditável.

---

## Épico 8 — Observabilidade e Confiabilidade (P1)

### US-8.1 Logs estruturados e correlação distribuída
**Descrição**: padronizar logs com trace_id/request_id.

**Critérios de aceite**:
- Logs com correlação entre gateway e serviços.
- Pesquisa por paciente/operação com trilha completa.
- Política de retenção de logs definida.

### US-8.2 Métricas e tracing
**Descrição**: instrumentação com métricas de negócio e técnicas.

**Critérios de aceite**:
- Dashboards de latência, erro e saturação publicados.
- Tracing distribuído ponta a ponta disponível.
- Alertas acionáveis com runbooks.

### US-8.3 SLO/SLI
**Descrição**: metas de confiabilidade por serviço.

**Critérios de aceite**:
- SLO definidos e monitorados.
- Budget de erro por serviço implementado.
- Alertas de violação em tempo real.

---

## Épico 9 — AI Service e MLOps (P1)

### US-9.1 Implementar AI Service desacoplado
**Descrição**: inferência para suporte clínico sem acoplamento ao EMR.

**Critérios de aceite**:
- Endpoint de inferência versionado.
- Timeout/circuit breaker e fallback clínico definidos.
- Auditoria de sugestão e explicabilidade mínima registrada.

### US-9.2 Pipeline de treino e registro de modelo
**Descrição**: ciclo de vida de modelo com governança.

**Critérios de aceite**:
- Dataset, experimento e modelo versionados.
- Critérios de promoção de modelo definidos.
- Reprodutibilidade do treino comprovada.

### US-9.3 Monitoramento de desempenho de modelo
**Descrição**: detectar drift e perda de performance.

**Critérios de aceite**:
- Métricas de drift e qualidade online disponíveis.
- Alertas para degradação significativa.
- Rollback para modelo anterior funcional.

---

## Épico 10 — Evidências Experimentais para o Artigo (P1)

### US-10.1 Plano experimental reprodutível
**Descrição**: cenários de carga, disponibilidade e recuperação.

**Critérios de aceite**:
- Scripts de benchmark versionados.
- Cenários reproduzíveis em homologação.
- Relatórios com metodologia e parâmetros.

### US-10.2 Métricas comparativas pré e pós arquitetura
**Descrição**: demonstrar ganhos de escalabilidade e operação.

**Critérios de aceite**:
- Métricas: latência, throughput, MTTR, disponibilidade, taxa de erro.
- Comparação com baseline antes da decomposição.
- Gráficos e tabelas prontos para publicação.

### US-10.3 Evidências de conformidade e segurança
**Descrição**: consolidar material para seção de resultados e discussão.

**Critérios de aceite**:
- Checklist LGPD preenchido com evidências técnicas.
- Evidências de segurança de pipeline e runtime.
- Relatório técnico consolidado para submissão.

---

## 5) Planejamento sugerido por sprints (8 sprints)

## Sprint 1
- Épico 1 (US-1.1, US-1.2)
- Épico 7 (US-7.1 baseline)
- Entrega: baseline arquitetural e pipeline de qualidade mínima.

## Sprint 2
- Épico 2 (US-2.1 Auth, US-2.2 Patient)
- Épico 4 (US-4.2 segurança básica)
- Entrega: autenticação central e serviço de paciente desacoplado.

## Sprint 3
- Épico 2 (US-2.3 EMR, Scheduling)
- Épico 3 (US-3.1)
- Entrega: núcleo clínico e agendamento por serviços independentes.

## Sprint 4
- Épico 2 (US-2.4 Audit)
- Épico 3 (US-3.2, US-3.3)
- Épico 4 (US-4.1)
- Entrega: auditoria e qualificação de dado clínico com codificação.

## Sprint 5
- Épico 5 (US-5.1, US-5.2, US-5.3)
- Épico 7 (US-7.2)
- Entrega: cadeia Docker + registry + segurança de artefatos.

## Sprint 6
- Épico 6 (US-6.1, US-6.2, US-6.3)
- Épico 7 (US-7.3)
- Entrega: deploy em Kubernetes com autoscaling, self-healing e rollback.

## Sprint 7
- Épico 8 (US-8.1, US-8.2, US-8.3)
- Épico 9 (US-9.1)
- Entrega: observabilidade completa e AI service inicial.

## Sprint 8
- Épico 9 (US-9.2, US-9.3)
- Épico 10 (US-10.1, US-10.2, US-10.3)
- Épico 4 (US-4.3)
- Entrega: MLOps maduro e pacote de evidências para resultados finais.

---

## 6) Definition of Done (DoD) global

Uma história só é concluída quando:
1. Código segue arquitetura definida e passa revisão técnica.
2. Testes automatizados relevantes passam (unitário/integrado/contrato).
3. Pipeline CI/CD executa sem falhas.
4. Requisitos de segurança/LGPD aplicáveis foram atendidos.
5. Observabilidade mínima (logs, métricas) está ativa para o incremento.
6. Documentação técnica e operacional foi atualizada.

---

## 7) Métricas de acompanhamento do backlog

### Fluxo
- Lead time por história.
- Throughput por sprint.
- Taxa de retrabalho.

### Qualidade
- Cobertura de testes por serviço.
- Defeitos em produção por release.
- Taxa de falha de deploy.

### Operação
- Disponibilidade por serviço.
- Latência p95/p99 de endpoints críticos.
- MTTR (tempo médio de recuperação).

### IA/MLOps
- Drift de dados/modelo.
- Acurácia/F1 por janela de monitoramento.
- Taxa de fallback do AI Service.

---

## 8) Riscos e mitigação

1. **Acoplamento indevido entre serviços**
   - Mitigação: revisão de contratos + testes de contrato obrigatórios.

2. **Complexidade operacional de Kubernetes**
   - Mitigação: começar em homolog com manifests mínimos e evoluir por camadas.

3. **Risco regulatório (LGPD)**
   - Mitigação: privacy by design, auditoria contínua e checklist de conformidade por release.

4. **Baixa qualidade de dados clínicos para IA**
   - Mitigação: validações RCOP/SOAP e curadoria de dataset.

5. **Dívida de observabilidade**
   - Mitigação: critérios de observabilidade no DoD desde os primeiros sprints.

---

## 9) Checklist de prontidão para início da execução

- [ ] ADRs iniciais aprovados.
- [ ] Template de microsserviço criado.
- [ ] Pipeline CI baseline configurado.
- [ ] Ambiente Docker local multi-serviço funcional.
- [ ] Segurança mínima (JWT, segredos, TLS em borda) definida.
- [ ] Plano de testes de contrato estabelecido.
- [ ] Estratégia de deploy em Kubernetes documentada.
- [ ] Plano de evidências experimentais acordado com orientador/equipe.

---

## 10) Observação final

Este backlog é vivo e deve ser revisado ao final de cada sprint com base em:
- métricas coletadas;
- riscos emergentes;
- lições aprendidas de operação;
- evolução dos requisitos clínicos e regulatórios.
