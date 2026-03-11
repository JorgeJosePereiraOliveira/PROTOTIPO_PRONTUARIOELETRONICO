from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.consent.consent_repository_interface import ConsentRepositoryInterface


@dataclass
class ListPatientConsentsInputDTO:
    patient_id: str


@dataclass
class ConsentListItemDTO:
    id: str
    patient_id: str
    legal_basis: str
    purpose: str
    status: str
    granted_at: str
    revoked_at: str | None


@dataclass
class ListPatientConsentsOutputDTO:
    consents: list[ConsentListItemDTO]


class ListPatientConsentsUseCase(
    UseCase[ListPatientConsentsInputDTO, ListPatientConsentsOutputDTO]
):
    def __init__(self, consent_repository: ConsentRepositoryInterface):
        self._consent_repository = consent_repository

    def execute(
        self,
        input_dto: ListPatientConsentsInputDTO,
    ) -> ListPatientConsentsOutputDTO:
        patient_id = input_dto.patient_id.strip()
        if not patient_id:
            raise ValueError("patient_id is required")

        items = sorted(
            self._consent_repository.find_by_patient_id(patient_id),
            key=lambda item: item.granted_at,
            reverse=True,
        )

        return ListPatientConsentsOutputDTO(
            consents=[
                ConsentListItemDTO(
                    id=item.id,
                    patient_id=item.patient_id,
                    legal_basis=item.legal_basis,
                    purpose=item.purpose,
                    status=item.status,
                    granted_at=item.granted_at,
                    revoked_at=item.revoked_at,
                )
                for item in items
            ]
        )
