# Context Map — PROTOTIPO_PRONTUARIOELETRONICO

- **Data:** 2026-03-04
- **Issue:** #1 (ARC-01)

## Contextos definidos

1. **Auth**
   - Responsável por autenticação, emissão/validação de token e perfis de acesso.
2. **Patient**
   - Cadastro e atualização de dados demográficos do paciente.
3. **EMR**
   - Núcleo clínico: RCOP/SOAP, problemas clínicos e evolução.
4. **Scheduling**
   - Agenda e gestão de consultas.
5. **Audit**
   - Trilhas de auditoria para eventos críticos.
6. **AI**
   - Inferência e apoio à decisão clínica (desacoplado do EMR).

## Ownership de dados

- Auth: usuários, credenciais, perfis.
- Patient: dados cadastrais do paciente.
- EMR: registros clínicos, SOAP, problemas.
- Scheduling: compromissos e status de agenda.
- Audit: eventos auditáveis e rastros.
- AI: metadados de inferência e versões de modelo.

## Integrações permitidas (alto nível)

- Auth -> (todos os demais): autorização/autenticação.
- Patient <-> EMR: referência a paciente por identificador.
- Scheduling -> Patient/Auth: validação de identidade/perfil.
- EMR -> AI: chamada de inferência com fallback seguro.
- Todos -> Audit: publicação de eventos críticos.

## Integrações proibidas

- Acesso direto ao banco de dados de outro contexto.
- Dependência de código interno entre contextos (sem contrato).
- AI alterando dados clínicos primários do EMR sem caso de uso explícito.

## Contratos e versionamento

- Toda integração deve expor contrato versionado.
- Mudanças breaking devem ser tratadas por nova versão de endpoint/evento.

## Dependências arquiteturais internas (por contexto)

- `infra -> application -> domain` (obrigatório).
- `domain` deve permanecer puro (sem framework/ORM).
