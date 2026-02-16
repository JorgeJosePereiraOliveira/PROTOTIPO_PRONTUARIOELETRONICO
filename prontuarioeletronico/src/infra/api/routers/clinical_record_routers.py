"""
Clinical Record API Routers
Handles HTTP requests related to clinical record operations
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ....application.clinical_record.register_soap_usecase import (
    RegisterSOAPUseCase,
    RegisterSOAPDTO
)
from ....application.clinical_record.create_problem_usecase import (
    CreateProblemUseCase,
    CreateProblemDTO
)
from ....infra.clinical_record.sqlalchemy.clinical_record_repository import ClinicalRecordRepository
from ....infra.api.database import get_db
from ..presenters.clinical_record_presenter import RegisterSOAPRequest, CreateProblemRequest


router = APIRouter(prefix="/api/v1/clinical-records", tags=["clinical-records"])


@router.post("/soap", response_model=dict)
def register_soap_note(
    soap_data: RegisterSOAPRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new SOAP clinical note.
    
    SOAP stands for:
    - S: Subjective (patient's symptoms and concerns)
    - O: Objective (clinical findings and test results)
    - A: Assessment (diagnosis and clinical impression)
    - P: Plan (treatment and follow-up)
    """
    # Initialize repository and use case
    repository = ClinicalRecordRepository(db)
    use_case = RegisterSOAPUseCase(repository)
    
    # Create input DTO
    input_dto = RegisterSOAPDTO(
        patient_id=soap_data.patient_id,
        professional_id=soap_data.professional_id,
        problem_id=soap_data.problem_id,
        encounter_date=soap_data.encounter_date,
        patient_complaint=soap_data.patient_complaint,
        vital_signs=soap_data.vital_signs,
        physical_examination=soap_data.physical_examination,
        diagnosis=soap_data.diagnosis,
        treatment_plan=soap_data.treatment_plan,
        medical_history=soap_data.medical_history,
        lab_results=soap_data.lab_results,
        medications=soap_data.medications,
        allergies=soap_data.allergies,
        clinical_impression=soap_data.clinical_impression
    )
    
    # Execute use case
    output_dto = use_case.execute(input_dto)
    
    return {
        "clinical_record_id": output_dto.clinical_record_id,
        "message": output_dto.message
    }


@router.post("/problems", response_model=dict)
def create_problem(
    problem_data: CreateProblemRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new clinical problem.
    
    Problems are the central axis of the RCOP (Problem-Oriented Clinical Record).
    Each SOAP note is documented in relation to a specific problem.
    """
    repository = ClinicalRecordRepository(db)
    use_case = CreateProblemUseCase(repository)
    
    # Create input DTO
    input_dto = CreateProblemDTO(
        patient_id=problem_data.patient_id,
        description=problem_data.description,
        icd10_code=problem_data.icd10_code
    )
    
    # Execute use case
    output_dto = use_case.execute(input_dto)
    
    return {
        "problem_id": output_dto.problem_id,
        "message": output_dto.message
    }
