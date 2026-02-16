"""
Use Case: Register a new SOAP clinical note
Creates a complete clinical record following the SOAP structure
"""

from typing import Optional
from datetime import datetime
from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.clinical_record.rcop_soap import (
    ClinicalRecord, Subjective, Objective, Assessment, Plan
)


class RegisterSOAPDTO:
    """Data Transfer Object for registering a SOAP note"""
    
    def __init__(
        self,
        patient_id: str,
        professional_id: str,
        problem_id: str,
        encounter_date: datetime,
        patient_complaint: str,
        vital_signs: str,
        physical_examination: str,
        diagnosis: str,
        treatment_plan: str,
        medical_history: Optional[str] = None,
        lab_results: Optional[str] = None,
        medications: Optional[str] = None,
        allergies: Optional[str] = None,
        clinical_impression: Optional[str] = None
    ):
        self.patient_id = patient_id
        self.professional_id = professional_id
        self.problem_id = problem_id
        self.encounter_date = encounter_date
        self.patient_complaint = patient_complaint
        self.vital_signs = vital_signs
        self.physical_examination = physical_examination
        self.diagnosis = diagnosis
        self.treatment_plan = treatment_plan
        self.medical_history = medical_history
        self.lab_results = lab_results
        self.medications = medications
        self.allergies = allergies
        self.clinical_impression = clinical_impression


class RegisterSOAPOutputDTO:
    """Data Transfer Object for SOAP registration output"""
    
    def __init__(self, clinical_record_id: str, message: str):
        self.clinical_record_id = clinical_record_id
        self.message = message


class RegisterSOAPUseCase(UseCase[RegisterSOAPDTO, RegisterSOAPOutputDTO]):
    """
    Use Case for registering a new SOAP clinical note.
    
    This use case orchestrates the creation of a complete clinical record
    with all SOAP components (Subjective, Objective, Assessment, Plan).
    
    It represents a fundamental business operation: documenting a clinical encounter.
    """
    
    def __init__(self, clinical_record_repository):
        self._repository = clinical_record_repository
    
    def execute(self, input_dto: RegisterSOAPDTO) -> RegisterSOAPOutputDTO:
        """
        Execute the use case to register a SOAP note.
        
        Args:
            input_dto: Input data containing all SOAP components
            
        Returns:
            RegisterSOAPOutputDTO: Result with the created clinical record ID
            
        Raises:
            Exception: If validation fails or repository operation fails
        """
        # Validate input
        self._validate_input(input_dto)
        
        # Create SOAP components
        subjective = Subjective(
            id=self._generate_id(),
            clinical_record_id=self._generate_id(),  # Will be updated when record is created
            patient_complaint=input_dto.patient_complaint,
            medical_history=input_dto.medical_history,
            medications=input_dto.medications,
            allergies=input_dto.allergies
        )
        
        objective = Objective(
            id=self._generate_id(),
            clinical_record_id=self._generate_id(),
            vital_signs=input_dto.vital_signs,
            physical_examination=input_dto.physical_examination,
            lab_results=input_dto.lab_results
        )
        
        assessment = Assessment(
            id=self._generate_id(),
            clinical_record_id=self._generate_id(),
            diagnosis=input_dto.diagnosis,
            clinical_impression=input_dto.clinical_impression or input_dto.diagnosis,
            related_problems=[input_dto.problem_id]
        )
        
        plan = Plan(
            id=self._generate_id(),
            clinical_record_id=self._generate_id(),
            treatment_plan=input_dto.treatment_plan,
            medications=input_dto.medications
        )
        
        # Create the clinical record
        clinical_record = ClinicalRecord(
            id=self._generate_id(),
            patient_id=input_dto.patient_id,
            professional_id=input_dto.professional_id,
            problem_id=input_dto.problem_id,
            encounter_date=input_dto.encounter_date,
            subjective=subjective,
            objective=objective,
            assessment=assessment,
            plan=plan
        )
        
        # Persist the record
        self._repository.add(clinical_record)
        
        return RegisterSOAPOutputDTO(
            clinical_record_id=clinical_record.id,
            message="SOAP clinical record registered successfully"
        )
    
    def _validate_input(self, input_dto: RegisterSOAPDTO):
        """Validate input data according to business rules"""
        if not input_dto.patient_id:
            raise ValueError("Patient ID is required")
        if not input_dto.professional_id:
            raise ValueError("Professional ID is required")
        if not input_dto.problem_id:
            raise ValueError("Problem ID is required")
        if not input_dto.patient_complaint:
            raise ValueError("Patient complaint is required")
        if not input_dto.diagnosis:
            raise ValueError("Diagnosis is required")
    
    def _generate_id(self) -> str:
        """Generate a unique ID - should use a proper UUID library in production"""
        import uuid
        return str(uuid.uuid4())
