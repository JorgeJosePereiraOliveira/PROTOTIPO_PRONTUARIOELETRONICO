# ARC-02 — Template Base de Microsserviço (Clean Architecture)

Este template implementa o baseline definido em ARC-01:

- Regra da dependência: `infra -> application -> domain`
- Bounded context por serviço
- Testes mínimos obrigatórios no bootstrap

## Arquivo principal

- `templates/create_microservice.py`

## Como gerar um novo serviço

Na raiz de `prontuarioeletronico/`:

```bash
python templates/create_microservice.py --service-name auth
```

Por padrão, o serviço é criado em:

```text
services/auth-service/
```

Você também pode escolher o diretório de saída:

```bash
python templates/create_microservice.py --service-name patient --output-dir services
```

## Estrutura gerada

```text
<service>-service/
├── src/<service>/
│   ├── domain/
│   │   ├── __seedwork/
│   │   └── sample/
│   ├── application/sample/
│   └── infra/
│       ├── api/
│       └── sample/
├── tests/
├── requirements.txt
├── run_tests.py
├── Dockerfile
└── README.md
```

## Testes mínimos do template

Após gerar um serviço:

```bash
cd services/<service>-service
pip install -r requirements.txt
pytest -q
```

Cobertura mínima entregue pelo template:

- Caso de uso base (`CreateSampleUseCase`)
- Endpoint de saúde (`GET /health`)

## Conformidade com a baseline

O template já nasce compatível com:

- `board/ADR-001-clean-architecture.md`
- `board/CONTEXT_MAP.md`
- `board/ARQUITETURA_BASELINE.md`

Use este template como ponto de partida para Auth, Patient, EMR, Scheduling, Audit e AI, mantendo contratos explícitos entre contextos.
