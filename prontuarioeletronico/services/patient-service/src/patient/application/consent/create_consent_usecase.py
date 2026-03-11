from dataclasses import dataclass
from uuid import uuid4

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.consent.consent_entity import Consent
from ...domain.consent.consent_repository_interface import ConsentRepositoryInterface
from ...domain.patient.patient_repository_interface import PatientRepositoryInterface


@dataclass
class CreateConsentInputDTO:
    patient_id: str
    legal_basis: str
    purpose: str


@dataclass
class CreateConsentOutputDTO:
    id: str
    patient_id: str
    legal_basis: str
    purpose: str
    status: str
    granted_at: str
    revoked_at: str | None


class CreateConsentUseCase(UseCase[CreateConsentInputDTO, CreateConsentOutputDTO]):
    def __init__(
        self,
        consent_repository: ConsentRepositoryInterface,
        patient_repository: PatientRepositoryInterface,
    ):
        self._consent_repository = consent_repository
        self._patient_repository = patient_repository

    def execute(self, input_dto: CreateConsentInputDTO) -> CreateConsentOutputDTO:
        patient_id = input_dto.patient_id.strip()
        legal_basis = input_dto.legal_basis.strip().lower()
        purpose = input_dto.purpose.strip()

        if not patient_id:
            raise ValueError("patient_id is required")
        if not legal_basis:
            raise ValueError("legal_basis is required")
        if len(purpose) < 3:
            raise ValueError("purpose must have at least 3 characters")

        if self._patient_repository.find_by_id(patient_id) is None:
            raise ValueError("patient not found")

        for item in self._consent_repository.find_by_patient_id(patient_id):
            if item.status == "active" and item.purpose.casefold() == purpose.casefold():
                raise ValueError("active consent already exists for this purpose")

        entity = Consent(
            id=str(uuid4()),
            patient_id=patient_id,
            legal_basis=legal_basis,
            purpose=purpose,
            status="active",
            granted_at=Consent.utc_now_iso(),
            revoked_at=None,
        )
        self._consent_repository.add(entity)

        return CreateConsentOutputDTO(
            id=entity.id,
            patient_id=entity.patient_id,
            legal_basis=entity.legal_basis,
            purpose=entity.purpose,
            status=entity.status,
            granted_at=entity.granted_at,
            revoked_at=entity.revoked_at,
        )
