# ARC-02 — Entrega do Template Base de Microsserviço

- **Data:** 2026-03-04
- **Issue:** ARC-02
- **Dependência:** ARC-01

## Entregáveis

1. Gerador de microsserviço base:
   - `templates/create_microservice.py`
2. Guia de uso do template:
   - `templates/README_TEMPLATE_MICROSSERVICO.md`

## Critérios de aceite cobertos

### 1) Template de serviço disponível no repositório
- Atendido via pasta `templates/` com gerador versionado.

### 2) Novo serviço criado em < 30 min com testes mínimos passando
- Geração automática por comando único:
  - `python templates/create_microservice.py --service-name <nome>`
- Testes mínimos entregues no serviço gerado:
  - `tests/test_create_sample_usecase.py`
  - `tests/test_health_endpoint.py`

### 3) Convenções de pastas, naming e contratos documentadas
- Documentação operacional em:
  - `templates/README_TEMPLATE_MICROSSERVICO.md`
- Convenções incorporadas:
  - Nome do pacote sanitizado para `snake_case`
  - Estrutura por camadas (`domain`, `application`, `infra`)
  - Seedwork de `Entity`, `RepositoryInterface`, `UseCase`

## Observação

A estrutura gerada é base e intencionalmente mínima para acelerar bootstrap de serviços dos contextos do `CONTEXT_MAP` sem violar o baseline arquitetural.
