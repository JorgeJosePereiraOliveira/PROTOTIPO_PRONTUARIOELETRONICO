from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.professional.professional_repository_interface import (
    ProfessionalRepositoryInterface,
)


@dataclass
class ActivateProfessionalInputDTO:
    id: str


@dataclass
class ActivateProfessionalOutputDTO:
    id: str
    status: str
    updated_at: str


class ActivateProfessionalUseCase(
    UseCase[ActivateProfessionalInputDTO, ActivateProfessionalOutputDTO]
):
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: ActivateProfessionalInputDTO) -> ActivateProfessionalOutputDTO:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            raise ValueError("professional not found")

        entity.activate()
        self._repository.update(entity)

        return ActivateProfessionalOutputDTO(
            id=entity.id,
            status=entity.status,
            updated_at=entity.updated_at,
        )
