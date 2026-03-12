from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.professional.professional_entity import Professional
from ...domain.professional.professional_repository_interface import (
    ProfessionalRepositoryInterface,
)


@dataclass
class RegisterProfessionalInputDTO:
    full_name: str
    document_cpf: str
    council_type: str
    council_uf: str
    council_number: str
    occupation: str
    specialty: str | None = None
    auth_user_id: str | None = None


@dataclass
class RegisterProfessionalOutputDTO:
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


class RegisterProfessionalUseCase(
    UseCase[RegisterProfessionalInputDTO, RegisterProfessionalOutputDTO]
):
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self._repository = repository

    def execute(self, input_dto: RegisterProfessionalInputDTO) -> RegisterProfessionalOutputDTO:
        full_name = input_dto.full_name.strip()
        document_cpf = input_dto.document_cpf.strip()
        council_type = input_dto.council_type.strip().upper()
        council_uf = input_dto.council_uf.strip().upper()
        council_number = input_dto.council_number.strip().upper()
        occupation = input_dto.occupation.strip().lower()
        specialty = input_dto.specialty.strip() if input_dto.specialty else None
        auth_user_id = input_dto.auth_user_id.strip() if input_dto.auth_user_id else None

        if len(full_name) < 3:
            raise ValueError("full_name must have at least 3 characters")
        if not document_cpf.isdigit() or len(document_cpf) != 11:
            raise ValueError("document_cpf must contain 11 numeric digits")
        if len(council_type) < 2:
            raise ValueError("council_type must have at least 2 characters")
        if len(council_uf) != 2 or not council_uf.isalpha():
            raise ValueError("council_uf must be a 2-letter state code")
        if len(council_number) < 3:
            raise ValueError("council_number must have at least 3 characters")
        if len(occupation) < 3:
            raise ValueError("occupation must have at least 3 characters")

        existing = self._repository.find_by_council(council_type, council_uf, council_number)
        if existing is not None:
            raise ValueError("professional already registered for council")

        now = _iso_utc_now()
        entity = Professional(
            id=str(uuid4()),
            full_name=full_name,
            document_cpf=document_cpf,
            council_type=council_type,
            council_uf=council_uf,
            council_number=council_number,
            occupation=occupation,
            specialty=specialty,
            auth_user_id=auth_user_id,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self._repository.add(entity)

        return RegisterProfessionalOutputDTO(
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


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
