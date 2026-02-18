"""
RCOP (Registro Clínico Orientado por Problemas) - Problem-Oriented Clinical Record
Core domain entity that represents the clinical record structure as specified in the
medical protocol for problem-oriented clinical documentation.
"""

from typing import List, Optional
from datetime import datetime
from prontuarioeletronico.src.domain.__seedwork.entity import Entity


class Problem(Entity):
    """
    Represents a clinical problem within the RCOP system.
    
    A problem is a medical diagnosis or condition that requires monitoring
    and treatment. It is the central axis around which SOAP notes are organized.
    
    Attributes:
        id: Unique identifier for the problem
        patient_id: Reference to the patient
        description: Clinical description of the problem
        icd10_code: ICD-10 code for the problem (optional)
        status: Active, resolved, or archived
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    
    def __init__(
        self,
        id: str,
        patient_id: str,
        description: str,
        icd10_code: Optional[str] = None,
        status: str = "active",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        super().__init__(id)
        self._patient_id = patient_id
        self._description = description
        self._icd10_code = icd10_code
        self._status = status  # active, resolved, archived
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()
    
    @property
    def patient_id(self) -> str:
        return self._patient_id
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def icd10_code(self) -> Optional[str]:
        return self._icd10_code
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def resolve_problem(self):
        """Mark the problem as resolved."""
        if self._status != "resolved":
            self._status = "resolved"
            self._updated_at = datetime.now()
    
    def archive_problem(self):
        """Archive the problem."""
        if self._status != "archived":
            self._status = "archived"
            self._updated_at = datetime.now()
    
    def update_description(self, new_description: str):
        """Update the problem description."""
        self._description = new_description
        self._updated_at = datetime.now()


class Subjective(Entity):
    """
    Represents the 'Subjective' (S) component of the SOAP note.
    
    Contains the patient's reported symptoms, concerns, and medical history
    relevant to the clinical encounter.
    """
    
    def __init__(
        self,
        id: str,
        clinical_record_id: str,
        patient_complaint: str,
        medical_history: Optional[str] = None,
        medications: Optional[str] = None,
        allergies: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        super().__init__(id)
        self._clinical_record_id = clinical_record_id
        self._patient_complaint = patient_complaint
        self._medical_history = medical_history
        self._medications = medications
        self._allergies = allergies
        self._created_at = created_at or datetime.now()
    
    @property
    def clinical_record_id(self) -> str:
        return self._clinical_record_id
    
    @property
    def patient_complaint(self) -> str:
        return self._patient_complaint
    
    @property
    def medical_history(self) -> Optional[str]:
        return self._medical_history
    
    @property
    def medications(self) -> Optional[str]:
        return self._medications
    
    @property
    def allergies(self) -> Optional[str]:
        return self._allergies
    
    @property
    def created_at(self) -> datetime:
        return self._created_at


class Objective(Entity):
    """
    Represents the 'Objective' (O) component of the SOAP note.
    
    Contains measurable clinical findings from the physical examination
    and diagnostic tests.
    """
    
    def __init__(
        self,
        id: str,
        clinical_record_id: str,
        vital_signs: str,
        physical_examination: str,
        lab_results: Optional[str] = None,
        imaging_results: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        super().__init__(id)
        self._clinical_record_id = clinical_record_id
        self._vital_signs = vital_signs
        self._physical_examination = physical_examination
        self._lab_results = lab_results
        self._imaging_results = imaging_results
        self._created_at = created_at or datetime.now()
    
    @property
    def clinical_record_id(self) -> str:
        return self._clinical_record_id
    
    @property
    def vital_signs(self) -> str:
        return self._vital_signs
    
    @property
    def physical_examination(self) -> str:
        return self._physical_examination
    
    @property
    def lab_results(self) -> Optional[str]:
        return self._lab_results
    
    @property
    def imaging_results(self) -> Optional[str]:
        return self._imaging_results
    
    @property
    def created_at(self) -> datetime:
        return self._created_at


class Assessment(Entity):
    """
    Represents the 'Assessment' (A) component of the SOAP note.
    
    Contains the clinical evaluation and interpretation of findings,
    including the diagnosis or clinical impression.
    """
    
    def __init__(
        self,
        id: str,
        clinical_record_id: str,
        diagnosis: str,
        clinical_impression: str,
        differential_diagnoses: Optional[str] = None,
        related_problems: Optional[List[str]] = None,
        created_at: Optional[datetime] = None
    ):
        super().__init__(id)
        self._clinical_record_id = clinical_record_id
        self._diagnosis = diagnosis
        self._clinical_impression = clinical_impression
        self._differential_diagnoses = differential_diagnoses
        self._related_problems = related_problems or []
        self._created_at = created_at or datetime.now()
    
    @property
    def clinical_record_id(self) -> str:
        return self._clinical_record_id
    
    @property
    def diagnosis(self) -> str:
        return self._diagnosis
    
    @property
    def clinical_impression(self) -> str:
        return self._clinical_impression
    
    @property
    def differential_diagnoses(self) -> Optional[str]:
        return self._differential_diagnoses
    
    @property
    def related_problems(self) -> List[str]:
        return self._related_problems
    
    @property
    def created_at(self) -> datetime:
        return self._created_at


class Plan(Entity):
    """
    Represents the 'Plan' (P) component of the SOAP note.
    
    Contains the treatment plan, medications, procedures, and follow-up
    recommendations.
    """
    
    def __init__(
        self,
        id: str,
        clinical_record_id: str,
        treatment_plan: str,
        medications: Optional[str] = None,
        procedures: Optional[str] = None,
        follow_up: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        super().__init__(id)
        self._clinical_record_id = clinical_record_id
        self._treatment_plan = treatment_plan
        self._medications = medications
        self._procedures = procedures
        self._follow_up = follow_up
        self._created_at = created_at or datetime.now()
    
    @property
    def clinical_record_id(self) -> str:
        return self._clinical_record_id
    
    @property
    def treatment_plan(self) -> str:
        return self._treatment_plan
    
    @property
    def medications(self) -> Optional[str]:
        return self._medications
    
    @property
    def procedures(self) -> Optional[str]:
        return self._procedures
    
    @property
    def follow_up(self) -> Optional[str]:
        return self._follow_up
    
    @property
    def created_at(self) -> datetime:
        return self._created_at


class ClinicalRecord(Entity):
    """
    Represents a Clinical Record following the SOAP format.
    
    A clinical record is the complete documentation of a single clinical
    encounter, organized according to the SOAP structure (Subjective,
    Objective, Assessment, Plan).
    
    Attributes:
        id: Unique identifier for the record
        patient_id: Reference to the patient
        professional_id: Reference to the healthcare professional
        encounter_date: Date and time of the clinical encounter
        problem_id: Reference to the associated clinical problem
        subjective: Subjective component
        objective: Objective component
        assessment: Assessment component
        plan: Plan component
    """
    
    def __init__(
        self,
        id: str,
        patient_id: str,
        professional_id: str,
        problem_id: str,
        encounter_date: datetime,
        subjective: Optional[Subjective] = None,
        objective: Optional[Objective] = None,
        assessment: Optional[Assessment] = None,
        plan: Optional[Plan] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        super().__init__(id)
        self._patient_id = patient_id
        self._professional_id = professional_id
        self._problem_id = problem_id
        self._encounter_date = encounter_date
        self._subjective = subjective
        self._objective = objective
        self._assessment = assessment
        self._plan = plan
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()
    
    @property
    def patient_id(self) -> str:
        return self._patient_id
    
    @property
    def professional_id(self) -> str:
        return self._professional_id
    
    @property
    def problem_id(self) -> str:
        return self._problem_id
    
    @property
    def encounter_date(self) -> datetime:
        return self._encounter_date
    
    @property
    def subjective(self) -> Optional[Subjective]:
        return self._subjective
    
    @property
    def objective(self) -> Optional[Objective]:
        return self._objective
    
    @property
    def assessment(self) -> Optional[Assessment]:
        return self._assessment
    
    @property
    def plan(self) -> Optional[Plan]:
        return self._plan
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def set_subjective(self, subjective: Subjective):
        """Set or update the subjective component."""
        self._subjective = subjective
        self._updated_at = datetime.now()
    
    def set_objective(self, objective: Objective):
        """Set or update the objective component."""
        self._objective = objective
        self._updated_at = datetime.now()
    
    def set_assessment(self, assessment: Assessment):
        """Set or update the assessment component."""
        self._assessment = assessment
        self._updated_at = datetime.now()
    
    def set_plan(self, plan: Plan):
        """Set or update the plan component."""
        self._plan = plan
        self._updated_at = datetime.now()
    
    def is_complete(self) -> bool:
        """Check if the SOAP record has all required components."""
        return (
            self._subjective is not None
            and self._objective is not None
            and self._assessment is not None
            and self._plan is not None
        )
