# ADR-001 — Clean Architecture por Contexto de Serviço

- **Status:** Aprovado
- **Data:** 2026-03-04
- **Issue:** #1 (ARC-01)
- **Escopo:** PROTOTIPO_PRONTUARIOELETRONICO

## Contexto

O projeto evolui de uma base monolítica modular para uma arquitetura orientada a microsserviços com rastreabilidade por sprint. É necessário padronizar o desenho técnico para manter baixo acoplamento, alta testabilidade e previsibilidade de evolução.

## Decisão

Cada contexto de negócio deve seguir internamente a estrutura de Clean Architecture:

- `domain/` — entidades e regras de negócio puras.
- `application/` — casos de uso e orquestração.
- `infra/` — adaptadores (API, persistência, mensageria, integrações).

Regra de dependência obrigatória:

- Dependências sempre de fora para dentro:
  - `infra -> application -> domain`
- `domain` não depende de framework/banco/transporte.
- Contratos de porta/repositório são definidos em camadas internas.

## Consequências

### Positivas
- Isolamento de regras clínicas (RCOP/SOAP) de tecnologia.
- Maior testabilidade unitária e de contrato.
- Redução de impacto de mudanças de infraestrutura.

### Custos
- Maior disciplina de design e revisão de PR.
- Necessidade de documentação mínima (ADRs e context map).

## Regras de revisão (gate)

Um PR é reprovado se:
- Introduzir import de `infra` dentro de `domain`.
- Acoplar caso de uso diretamente a framework específico.
- Persistir lógica de negócio em camada de controller/repositório.

## Relação com próximos passos

Este ADR desbloqueia:
- ARC-02 (template de microsserviço)
- CICD-01 (pipeline com checks arquiteturais)
