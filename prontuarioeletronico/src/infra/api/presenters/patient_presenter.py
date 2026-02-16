"""
DTOs for Patient API Requests and Responses
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PatientCreateRequest(BaseModel):
    """Request DTO for creating a new patient"""
    name: str
    date_of_birth: datetime
    gender: str  # M, F, O, N
    cpf: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    insurance: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva",
                "date_of_birth": "1990-05-15T00:00:00",
                "gender": "M",
                "cpf": "12345678901",
                "email": "joao@example.com",
                "phone": "11999999999",
                "address": "Rua A, 123",
                "city": "São Paulo",
                "state": "SP",
                "insurance": "Unimed"
            }
        }


class PatientResponse(BaseModel):
    """Response DTO for patient data"""
    id: str
    name: str
    date_of_birth: datetime
    gender: str
    cpf: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    insurance: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
