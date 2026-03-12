from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.professional.professional_repository_interface import (
    ProfessionalRepositoryInterface,
)


@dataclass
class DeactivateProfessionalInputDTO:
    id: str


@dataclass
class DeactivateProfessionalOutputDTO:
    id: str
    status: str
    updated_at: str


class DeactivateProfessionalUseCase(
    UseCase[DeactivateProfessionalInputDTO, DeactivateProfessionalOutputDTO]
):
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: DeactivateProfessionalInputDTO) -> DeactivateProfessionalOutputDTO:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            raise ValueError("professional not found")

        entity.deactivate()
        self._repository.update(entity)

        return DeactivateProfessionalOutputDTO(
            id=entity.id,
            status=entity.status,
            updated_at=entity.updated_at,
        )
