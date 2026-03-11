from dataclasses import dataclass
from uuid import uuid4

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.emr.problem_repository_interface import ProblemRepositoryInterface
from ...domain.emr.soap_record_entity import SOAPRecord
from ...domain.emr.soap_repository_interface import SOAPRepositoryInterface


@dataclass
class CreateSOAPInputDTO:
    problem_id: str
    patient_id: str
    professional_id: str
    subjective: str
    objective: str
    assessment: str
    plan: str


@dataclass
class CreateSOAPOutputDTO:
    id: str
    problem_id: str
    patient_id: str
    professional_id: str
    subjective: str
    objective: str
    assessment: str
    plan: str
    created_at: str


class CreateSOAPUseCase(UseCase[CreateSOAPInputDTO, CreateSOAPOutputDTO]):
    _MIN_CLINICAL_TEXT_LENGTH = 10
    _PLACEHOLDER_VALUES = {"n/a", "na", "-", ".", "sem dados"}

    def __init__(
        self,
        soap_repository: SOAPRepositoryInterface,
        problem_repository: ProblemRepositoryInterface,
    ):
        self._soap_repository = soap_repository
        self._problem_repository = problem_repository

    def execute(self, input_dto: CreateSOAPInputDTO) -> CreateSOAPOutputDTO:
        problem_id = input_dto.problem_id.strip()
        patient_id = input_dto.patient_id.strip()
        professional_id = input_dto.professional_id.strip()
        subjective = input_dto.subjective.strip()
        objective = input_dto.objective.strip()
        assessment = input_dto.assessment.strip()
        plan = input_dto.plan.strip()

        if not problem_id:
            raise ValueError("problem_id is required")
        if not patient_id:
            raise ValueError("patient_id is required")
        if not professional_id:
            raise ValueError("professional_id is required")

        for field_name, value in {
            "subjective": subjective,
            "objective": objective,
            "assessment": assessment,
            "plan": plan,
        }.items():
            if value.casefold() in self._PLACEHOLDER_VALUES:
                raise ValueError(f"{field_name} cannot use placeholder values")
            if len(value) < self._MIN_CLINICAL_TEXT_LENGTH:
                raise ValueError(
                    f"{field_name} must have at least {self._MIN_CLINICAL_TEXT_LENGTH} characters"
                )

        normalized_sections = {
            "subjective": subjective.casefold(),
            "objective": objective.casefold(),
            "assessment": assessment.casefold(),
            "plan": plan.casefold(),
        }

        if normalized_sections["subjective"] == normalized_sections["objective"]:
            raise ValueError("subjective and objective must not be identical")
        if normalized_sections["assessment"] == normalized_sections["plan"]:
            raise ValueError("assessment and plan must not be identical")
        if normalized_sections["assessment"] == normalized_sections["subjective"]:
            raise ValueError("assessment must not be identical to subjective")
        if normalized_sections["assessment"] == normalized_sections["objective"]:
            raise ValueError("assessment must not be identical to objective")
        if normalized_sections["plan"] == normalized_sections["subjective"]:
            raise ValueError("plan must not be identical to subjective")
        if normalized_sections["plan"] == normalized_sections["objective"]:
            raise ValueError("plan must not be identical to objective")

        problem = self._problem_repository.find_by_id(problem_id)
        if problem is None:
            raise ValueError("problem not found")

        entity = SOAPRecord(
            id=str(uuid4()),
            problem_id=problem_id,
            patient_id=patient_id,
            professional_id=professional_id,
            subjective=subjective,
            objective=objective,
            assessment=assessment,
            plan=plan,
        )
        self._soap_repository.add(entity)

        return CreateSOAPOutputDTO(
            id=entity.id,
            problem_id=entity.problem_id,
            patient_id=entity.patient_id,
            professional_id=entity.professional_id,
            subjective=entity.subjective,
            objective=entity.objective,
            assessment=entity.assessment,
            plan=entity.plan,
            created_at=entity.created_at,
        )
