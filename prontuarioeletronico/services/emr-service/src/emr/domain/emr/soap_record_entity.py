from datetime import datetime, timezone

from ..__seedwork.entity import Entity


class SOAPRecord(Entity):
    def __init__(
        self,
        id: str,
        problem_id: str,
        patient_id: str,
        professional_id: str,
        subjective: str,
        objective: str,
        assessment: str,
        plan: str,
        created_at: str | None = None,
    ):
        super().__init__(id=id)
        self._problem_id = problem_id
        self._patient_id = patient_id
        self._professional_id = professional_id
        self._subjective = subjective
        self._objective = objective
        self._assessment = assessment
        self._plan = plan
        self._created_at = created_at or datetime.now(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )

    @property
    def problem_id(self) -> str:
        return self._problem_id

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @property
    def professional_id(self) -> str:
        return self._professional_id

    @property
    def subjective(self) -> str:
        return self._subjective

    @property
    def objective(self) -> str:
        return self._objective

    @property
    def assessment(self) -> str:
        return self._assessment

    @property
    def plan(self) -> str:
        return self._plan

    @property
    def created_at(self) -> str:
        return self._created_at
