from dataclasses import dataclass

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.emr.problem_repository_interface import ProblemRepositoryInterface
from ...domain.emr.soap_repository_interface import SOAPRepositoryInterface


@dataclass
class ListProblemTimelineInputDTO:
    patient_id: str
    problem_id: str | None = None


@dataclass
class TimelineEventDTO:
    event_type: str
    event_id: str
    occurred_at: str
    patient_id: str
    problem_id: str
    payload: dict


@dataclass
class ListProblemTimelineOutputDTO:
    patient_id: str
    problem_id: str | None
    events: list[TimelineEventDTO]


class ListProblemTimelineUseCase(
    UseCase[ListProblemTimelineInputDTO, ListProblemTimelineOutputDTO]
):
    def __init__(
        self,
        problem_repository: ProblemRepositoryInterface,
        soap_repository: SOAPRepositoryInterface,
    ):
        self._problem_repository = problem_repository
        self._soap_repository = soap_repository

    def execute(self, input_dto: ListProblemTimelineInputDTO) -> ListProblemTimelineOutputDTO:
        patient_id = input_dto.patient_id.strip()
        problem_id = input_dto.problem_id.strip() if input_dto.problem_id else None

        if not patient_id:
            raise ValueError("patient_id is required")

        problems = [
            problem
            for problem in self._problem_repository.find_all()
            if problem.patient_id == patient_id
        ]

        if problem_id:
            selected_problem = next((problem for problem in problems if problem.id == problem_id), None)
            if selected_problem is None:
                raise ValueError("problem not found")
            selected_problems = [selected_problem]
        else:
            selected_problems = problems

        selected_problem_ids = {problem.id for problem in selected_problems}

        events: list[TimelineEventDTO] = []
        for problem in selected_problems:
            events.append(
                TimelineEventDTO(
                    event_type="problem",
                    event_id=problem.id,
                    occurred_at=problem.created_at,
                    patient_id=problem.patient_id,
                    problem_id=problem.id,
                    payload={
                        "description": problem.description,
                        "status": problem.status,
                        "terminology_system": problem.terminology_system,
                        "terminology_code": problem.terminology_code,
                    },
                )
            )

        for soap in self._soap_repository.find_all():
            if soap.patient_id != patient_id or soap.problem_id not in selected_problem_ids:
                continue
            events.append(
                TimelineEventDTO(
                    event_type="soap",
                    event_id=soap.id,
                    occurred_at=soap.created_at,
                    patient_id=soap.patient_id,
                    problem_id=soap.problem_id,
                    payload={
                        "professional_id": soap.professional_id,
                        "subjective": soap.subjective,
                        "objective": soap.objective,
                        "assessment": soap.assessment,
                        "plan": soap.plan,
                    },
                )
            )

        events.sort(key=lambda item: (item.occurred_at, item.event_id))

        return ListProblemTimelineOutputDTO(
            patient_id=patient_id,
            problem_id=problem_id,
            events=events,
        )
