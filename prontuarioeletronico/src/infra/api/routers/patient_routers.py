"""
Patient API Routers
Handles HTTP requests related to patient operations
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ....application.patient.register_patient_usecase import (
    RegisterPatientUseCase,
    RegisterPatientDTO
)
from ....infra.patient.sqlalchemy.patient_repository import PatientRepository
from ....infra.api.database import get_db
from ..presenters.patient_presenter import PatientCreateRequest, PatientResponse


router = APIRouter(prefix="/api/v1/patients", tags=["patients"])


@router.post("/", response_model=dict)
def create_patient(
    patient_data: PatientCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new patient.
    
    This endpoint demonstrates the flow through clean architecture:
    1. HTTP Request (FastAPI Controller)
    2. Use Case Layer (Business Logic)
    3. Domain Layer (Entities)
    4. Repository (Persistence)
    5. HTTP Response
    """
    # Initialize repository and use case
    repository = PatientRepository(db)
    use_case = RegisterPatientUseCase(repository)
    
    # Create input DTO
    input_dto = RegisterPatientDTO(
        name=patient_data.name,
        date_of_birth=patient_data.date_of_birth,
        gender=patient_data.gender,
        cpf=patient_data.cpf,
        email=patient_data.email,
        phone=patient_data.phone,
        address=patient_data.address,
        city=patient_data.city,
        state=patient_data.state,
        insurance=patient_data.insurance
    )
    
    # Execute use case
    output_dto = use_case.execute(input_dto)
    
    return {
        "patient_id": output_dto.patient_id,
        "message": output_dto.message
    }


@router.get("/{patient_id}", response_model=dict)
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):
    """Get patient details by ID"""
    repository = PatientRepository(db)
    patient = repository.find_by_id(patient_id)
    
    if not patient:
        return {"error": "Patient not found"}
    
    return {
        "id": patient.id,
        "name": patient.name,
        "cpf": patient.cpf,
        "email": patient.email,
        "phone": patient.phone,
        "age": patient.calculate_age()
    }


@router.get("/", response_model=dict)
def list_patients(
    db: Session = Depends(get_db)
):
    """List all patients"""
    repository = PatientRepository(db)
    patients = repository.find_all()
    
    return {
        "total": len(patients),
        "patients": [
            {
                "id": p.id,
                "name": p.name,
                "cpf": p.cpf
            }
            for p in patients
        ]
    }
