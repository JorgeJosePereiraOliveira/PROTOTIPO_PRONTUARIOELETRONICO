# Arquitetura Baseline e Checklist de Conformidade

- **Data:** 2026-03-04
- **Issue:** #1 (ARC-01)

## Baseline adotada

- Arquitetura alvo: microsserviços orientados a contextos de negócio.
- Arquitetura interna de cada contexto: Clean Architecture.
- Integração entre contextos: API/eventos com contratos versionados.

## Checklist de conformidade arquitetural (PR)

### A. Regra da dependência
- [ ] Não há import de `infra` dentro de `domain`.
- [ ] Casos de uso (`application`) não dependem de framework específico.
- [ ] Entidades de domínio não dependem de ORM/web framework.

### B. Fronteiras de contexto
- [ ] O código não acessa banco de outro contexto.
- [ ] A comunicação entre contextos usa contrato explícito.
- [ ] IDs de referência entre contextos são tratados por contrato, não por acoplamento interno.

### C. Segurança e governança
- [ ] Operações críticas produzem evento para Audit.
- [ ] Requisitos de autenticação/autorização são respeitados via Auth.
- [ ] Mudanças breaking em contrato foram versionadas.

### D. Qualidade para merge
- [ ] Testes relevantes executados e verdes.
- [ ] Evidências anexadas na issue/PR.
- [ ] Documentação mínima atualizada (ADR/Context Map, quando aplicável).

## Critério de pronto da ARC-01

A issue #1 é considerada concluída quando:
1. ADR-001 publicado.
2. Context Map publicado com os 6 contextos.
3. Checklist de conformidade definido para revisão de PR.
4. Itens rastreáveis no board com evidência.

## Referências internas

- [ADR-001-clean-architecture.md](ADR-001-clean-architecture.md)
- [CONTEXT_MAP.md](CONTEXT_MAP.md)
- [README_BOARD_EXECUCAO.md](README_BOARD_EXECUCAO.md)
- [CHECKLIST_GO_LIVE_BOARD.md](CHECKLIST_GO_LIVE_BOARD.md)
