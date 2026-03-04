"""
ARC-02 - Gerador de template base para microsserviços em Clean Architecture.

Uso:
    python templates/create_microservice.py --service-name auth
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEMPLATE_FILES: dict[str, str] = {
    "README.md": """# {{SERVICE_TITLE}} Service

Microsserviço gerado a partir do template ARC-02 com Clean Architecture por contexto.

## Estrutura

```text
{{SERVICE_FOLDER}}/
├── src/
│   └── {{PACKAGE_NAME}}/
│       ├── domain/
│       ├── application/
│       └── infra/
├── tests/
├── requirements.txt
├── run_tests.py
└── Dockerfile
```

## Executar localmente

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
pytest -q
uvicorn src.{{PACKAGE_NAME}}.infra.api.main:app --reload --port 8001
```

## Endpoints base

- `GET /health` -> liveness/readiness
- `GET /api/v1/info` -> metadados do serviço
""",
    "requirements.txt": """fastapi==0.109.0
uvicorn==0.27.0
pytest==8.2.0
httpx==0.27.0
""",
    "run_tests.py": """import subprocess
import sys


if __name__ == \"__main__\":
    result = subprocess.run([sys.executable, \"-m\", \"pytest\", \"-q\"], check=False)
    raise SystemExit(result.returncode)
""",
    "Dockerfile": """FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

EXPOSE 8000
CMD [\"uvicorn\", \"src.{{PACKAGE_NAME}}.infra.api.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]
""",
    "src/{{PACKAGE_NAME}}/__init__.py": "",
    "src/{{PACKAGE_NAME}}/domain/__init__.py": "",
    "src/{{PACKAGE_NAME}}/domain/__seedwork/__init__.py": "",
    "src/{{PACKAGE_NAME}}/domain/__seedwork/entity.py": """from abc import ABC
from typing import Any


class Entity(ABC):
    def __init__(self, id: Any = None):
        self._id = id

    @property
    def id(self) -> Any:
        return self._id

    @id.setter
    def id(self, value: Any):
        self._id = value

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        if self._id is None or other._id is None:
            return self is other
        return self._id == other._id

    def __hash__(self):
        return hash(self._id) if self._id else hash(id(self))
""",
    "src/{{PACKAGE_NAME}}/domain/__seedwork/repository_interface.py": """from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from .entity import Entity


Entity_T = TypeVar(\"Entity_T\", bound=Entity)


class RepositoryInterface(ABC, Generic[Entity_T]):
    @abstractmethod
    def add(self, entity: Entity_T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: Entity_T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Entity_T]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Entity_T]:
        raise NotImplementedError
""",
    "src/{{PACKAGE_NAME}}/domain/__seedwork/use_case_interface.py": """from abc import ABC, abstractmethod
from typing import Generic, TypeVar


InputDTO = TypeVar(\"InputDTO\")
OutputDTO = TypeVar(\"OutputDTO\")


class UseCase(ABC, Generic[InputDTO, OutputDTO]):
    @abstractmethod
    def execute(self, input_dto: InputDTO) -> OutputDTO:
        raise NotImplementedError
""",
    "src/{{PACKAGE_NAME}}/domain/sample/__init__.py": "",
    "src/{{PACKAGE_NAME}}/domain/sample/sample_entity.py": """from ..__seedwork.entity import Entity


class SampleEntity(Entity):
    def __init__(self, id: str, name: str):
        super().__init__(id=id)
        self._name = name

    @property
    def name(self) -> str:
        return self._name
""",
    "src/{{PACKAGE_NAME}}/domain/sample/sample_repository_interface.py": """from ..__seedwork.repository_interface import RepositoryInterface
from .sample_entity import SampleEntity


class SampleRepositoryInterface(RepositoryInterface[SampleEntity]):
    pass
""",
    "src/{{PACKAGE_NAME}}/application/__init__.py": "",
    "src/{{PACKAGE_NAME}}/application/sample/__init__.py": "",
    "src/{{PACKAGE_NAME}}/application/sample/create_sample_usecase.py": """from dataclasses import dataclass
from uuid import uuid4

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.sample.sample_entity import SampleEntity
from ...domain.sample.sample_repository_interface import SampleRepositoryInterface


@dataclass
class CreateSampleInputDTO:
    name: str


@dataclass
class CreateSampleOutputDTO:
    id: str
    message: str


class CreateSampleUseCase(UseCase[CreateSampleInputDTO, CreateSampleOutputDTO]):
    def __init__(self, repository: SampleRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: CreateSampleInputDTO) -> CreateSampleOutputDTO:
        if not input_dto.name or len(input_dto.name.strip()) < 3:
            raise ValueError(\"name must have at least 3 characters\")

        entity = SampleEntity(id=str(uuid4()), name=input_dto.name.strip())
        self._repository.add(entity)

        return CreateSampleOutputDTO(
            id=entity.id,
            message=\"sample entity created successfully\",
        )
""",
    "src/{{PACKAGE_NAME}}/infra/__init__.py": "",
    "src/{{PACKAGE_NAME}}/infra/sample/__init__.py": "",
    "src/{{PACKAGE_NAME}}/infra/sample/in_memory_sample_repository.py": """from ...domain.sample.sample_entity import SampleEntity
from ...domain.sample.sample_repository_interface import SampleRepositoryInterface


class InMemorySampleRepository(SampleRepositoryInterface):
    def __init__(self):
        self._data: dict[str, SampleEntity] = {}

    def add(self, entity: SampleEntity) -> None:
        self._data[entity.id] = entity

    def update(self, entity: SampleEntity) -> None:
        self._data[entity.id] = entity

    def delete(self, id: str) -> None:
        self._data.pop(id, None)

    def find_by_id(self, id: str):
        return self._data.get(id)

    def find_all(self):
        return list(self._data.values())
""",
    "src/{{PACKAGE_NAME}}/infra/api/__init__.py": "",
    "src/{{PACKAGE_NAME}}/infra/api/main.py": """from fastapi import FastAPI


app = FastAPI(
    title=\"{{SERVICE_TITLE}} Service\",
    version=\"1.0.0\",
    description=\"Microsserviço base em Clean Architecture (ARC-02)\",
)


@app.get(\"/health\")
def health_check():
    return {\"status\": \"healthy\", \"service\": \"{{SERVICE_NAME}}\"}


@app.get(\"/api/v1/info\")
def service_info():
    return {
        \"service\": \"{{SERVICE_NAME}}\",
        \"architecture\": \"clean-architecture\",
        \"layers\": [\"domain\", \"application\", \"infra\"],
    }
""",
    "tests/test_create_sample_usecase.py": """from src.{{PACKAGE_NAME}}.application.sample.create_sample_usecase import (
    CreateSampleInputDTO,
    CreateSampleUseCase,
)
from src.{{PACKAGE_NAME}}.infra.sample.in_memory_sample_repository import (
    InMemorySampleRepository,
)


def test_create_sample_usecase_success():
    repository = InMemorySampleRepository()
    use_case = CreateSampleUseCase(repository)

    output = use_case.execute(CreateSampleInputDTO(name=\"example\"))

    assert output.id
    assert output.message == \"sample entity created successfully\"
    assert len(repository.find_all()) == 1


def test_create_sample_usecase_rejects_short_name():
    repository = InMemorySampleRepository()
    use_case = CreateSampleUseCase(repository)

    try:
        use_case.execute(CreateSampleInputDTO(name=\"ab\"))
        assert False, \"expected ValueError\"
    except ValueError as error:
        assert \"at least 3 characters\" in str(error)
""",
    "tests/test_health_endpoint.py": """from fastapi.testclient import TestClient

from src.{{PACKAGE_NAME}}.infra.api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get(\"/health\")

    assert response.status_code == 200
    body = response.json()
    assert body[\"status\"] == \"healthy\"
    assert body[\"service\"] == \"{{SERVICE_NAME}}\"
""",
}


def sanitize_name(raw_name: str) -> str:
    normalized = raw_name.strip().lower().replace("-", "_").replace(" ", "_")
    normalized = re.sub(r"[^a-z0-9_]", "", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    if not normalized:
        raise ValueError("service name is empty after normalization")
    if normalized[0].isdigit():
        normalized = f"svc_{normalized}"
    return normalized


def render_template(content: str, context: dict[str, str]) -> str:
    rendered = content
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def create_service(service_name: str, output_dir: Path) -> Path:
    package_name = sanitize_name(service_name)
    service_folder = f"{package_name}-service"
    service_root = output_dir / service_folder

    if service_root.exists():
        raise FileExistsError(f"service already exists: {service_root}")

    context = {
        "SERVICE_NAME": package_name,
        "PACKAGE_NAME": package_name,
        "SERVICE_TITLE": package_name.replace("_", " ").title(),
        "SERVICE_FOLDER": service_folder,
    }

    for relative_path, content in TEMPLATE_FILES.items():
        final_relative_path = render_template(relative_path, context)
        file_path = service_root / final_relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(render_template(content, context), encoding="utf-8")

    return service_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera um microsserviço base em Clean Architecture (ARC-02)."
    )
    parser.add_argument(
        "--service-name",
        required=True,
        help="Nome do contexto/serviço. Ex.: auth, patient, audit",
    )
    parser.add_argument(
        "--output-dir",
        default="services",
        help="Diretório onde o serviço será criado (default: services)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    service_root = create_service(
        service_name=args.service_name,
        output_dir=Path(args.output_dir),
    )

    print(f"[OK] Serviço criado em: {service_root}")
    print("[NEXT] Entre na pasta do serviço e execute:")
    print("       pip install -r requirements.txt")
    print("       pytest -q")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
