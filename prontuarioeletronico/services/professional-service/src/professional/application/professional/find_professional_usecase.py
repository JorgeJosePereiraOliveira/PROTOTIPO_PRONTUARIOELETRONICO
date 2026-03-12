from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.professional.professional_repository_interface import (
    ProfessionalRepositoryInterface,
)


@dataclass
class FindProfessionalInputDTO:
    id: str


@dataclass
class FindProfessionalOutputDTO:
    id: str
    full_name: str
    document_cpf: str
    council_type: str
    council_uf: str
    council_number: str
    occupation: str
    specialty: str | None
    auth_user_id: str | None
    status: str
    created_at: str
    updated_at: str


class FindProfessionalUseCase(UseCase[FindProfessionalInputDTO, FindProfessionalOutputDTO | None]):
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: FindProfessionalInputDTO) -> FindProfessionalOutputDTO | None:
        entity = self._repository.find_by_id(input_dto.id)
        if entity is None:
            return None

        return FindProfessionalOutputDTO(
            id=entity.id,
            full_name=entity.full_name,
            document_cpf=entity.document_cpf,
            council_type=entity.council_type,
            council_uf=entity.council_uf,
            council_number=entity.council_number,
            occupation=entity.occupation,
            specialty=entity.specialty,
            auth_user_id=entity.auth_user_id,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
