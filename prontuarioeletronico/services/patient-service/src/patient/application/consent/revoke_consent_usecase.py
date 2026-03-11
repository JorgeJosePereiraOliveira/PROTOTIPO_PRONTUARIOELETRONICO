from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.consent.consent_entity import Consent
from ...domain.consent.consent_repository_interface import ConsentRepositoryInterface


@dataclass
class RevokeConsentInputDTO:
    patient_id: str
    consent_id: str


@dataclass
class RevokeConsentOutputDTO:
    id: str
    patient_id: str
    legal_basis: str
    purpose: str
    status: str
    granted_at: str
    revoked_at: str | None


class RevokeConsentUseCase(UseCase[RevokeConsentInputDTO, RevokeConsentOutputDTO]):
    def __init__(self, consent_repository: ConsentRepositoryInterface):
        self._consent_repository = consent_repository

    def execute(self, input_dto: RevokeConsentInputDTO) -> RevokeConsentOutputDTO:
        patient_id = input_dto.patient_id.strip()
        consent_id = input_dto.consent_id.strip()

        if not patient_id:
            raise ValueError("patient_id is required")
        if not consent_id:
            raise ValueError("consent_id is required")

        entity = self._consent_repository.find_by_id(consent_id)
        if entity is None or entity.patient_id != patient_id:
            raise ValueError("consent not found")
        if entity.status == "revoked":
            raise ValueError("consent already revoked")

        revoked_entity = Consent(
            id=entity.id,
            patient_id=entity.patient_id,
            legal_basis=entity.legal_basis,
            purpose=entity.purpose,
            status="revoked",
            granted_at=entity.granted_at,
            revoked_at=Consent.utc_now_iso(),
        )
        self._consent_repository.update(revoked_entity)

        return RevokeConsentOutputDTO(
            id=revoked_entity.id,
            patient_id=revoked_entity.patient_id,
            legal_basis=revoked_entity.legal_basis,
            purpose=revoked_entity.purpose,
            status=revoked_entity.status,
            granted_at=revoked_entity.granted_at,
            revoked_at=revoked_entity.revoked_at,
        )
