from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.professional.professional_repository_interface import (
    ProfessionalRepositoryInterface,
)


@dataclass
class ListProfessionalsInputDTO:
    council_type: str | None = None
    council_uf: str | None = None
    council_number: str | None = None
    status: str | None = None


@dataclass
class ProfessionalListItemDTO:
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


@dataclass
class ListProfessionalsOutputDTO:
    professionals: list[ProfessionalListItemDTO]


class ListProfessionalsUseCase(UseCase[ListProfessionalsInputDTO, ListProfessionalsOutputDTO]):
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: ListProfessionalsInputDTO) -> ListProfessionalsOutputDTO:
        status = input_dto.status
        if status is not None:
            status = status.strip().lower()
            if status not in {"active", "inactive"}:
                raise ValueError("status must be one of: active, inactive")

        entities = self._repository.find_all_filtered(
            council_type=input_dto.council_type.strip().upper()
            if input_dto.council_type
            else None,
            council_uf=input_dto.council_uf.strip().upper() if input_dto.council_uf else None,
            council_number=input_dto.council_number.strip().upper()
            if input_dto.council_number
            else None,
            status=status,
        )

        return ListProfessionalsOutputDTO(
            professionals=[
                ProfessionalListItemDTO(
                    id=item.id,
                    full_name=item.full_name,
                    document_cpf=item.document_cpf,
                    council_type=item.council_type,
                    council_uf=item.council_uf,
                    council_number=item.council_number,
                    occupation=item.occupation,
                    specialty=item.specialty,
                    auth_user_id=item.auth_user_id,
                    status=item.status,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                )
                for item in entities
            ]
        )
