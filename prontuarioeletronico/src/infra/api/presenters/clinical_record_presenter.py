"""
DTOs for Clinical Record API Requests and Responses
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RegisterSOAPRequest(BaseModel):
    """Request DTO for registering a SOAP clinical note"""
    patient_id: str
    professional_id: str
    problem_id: str
    encounter_date: datetime
    patient_complaint: str
    vital_signs: str
    physical_examination: str
    diagnosis: str
    treatment_plan: str
    medical_history: Optional[str] = None
    lab_results: Optional[str] = None
    medications: Optional[str] = None
    allergies: Optional[str] = None
    clinical_impression: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "patient-123",
                "professional_id": "prof-456",
                "problem_id": "problem-789",
                "encounter_date": "2024-02-13T10:30:00",
                "patient_complaint": "Dor de cabeça persistente",
                "vital_signs": "PA: 120/80, FC: 70, FR: 16",
                "physical_examination": "Nenhuma alteração no exame físico",
                "diagnosis": "Cefaleia tensional",
                "treatment_plan": "Repouso e analgésico"
            }
        }


class CreateProblemRequest(BaseModel):
    """Request DTO for creating a new clinical problem"""
    patient_id: str
    description: str
    icd10_code: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "patient-123",
                "description": "Hipertensão arterial sistêmica",
                "icd10_code": "I10"
            }
        }


class ClinicalRecordResponse(BaseModel):
    """Response DTO for clinical record"""
    id: str
    patient_id: str
    professional_id: str
    problem_id: str
    encounter_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
