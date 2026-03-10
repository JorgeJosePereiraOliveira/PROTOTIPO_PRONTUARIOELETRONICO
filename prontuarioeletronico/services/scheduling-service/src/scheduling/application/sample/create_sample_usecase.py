from dataclasses import dataclass
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
            raise ValueError("name must have at least 3 characters")

        entity = SampleEntity(id=str(uuid4()), name=input_dto.name.strip())
        self._repository.add(entity)

        return CreateSampleOutputDTO(
            id=entity.id,
            message="sample entity created successfully",
        )
