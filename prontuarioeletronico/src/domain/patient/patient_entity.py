"""
Patient Domain Entity - Represents a patient/person in the system
"""

from typing import Optional
from datetime import datetime
from ...__seedwork.entity import Entity


class Patient(Entity):
    """
    Represents a patient in the electronic patient record system.
    
    This entity encapsulates the core attributes and business rules
    related to a patient/person.
    
    Attributes:
        id: Unique identifier (usually ID number)
        name: Full name of the patient
        date_of_birth: Date of birth
        gender: Gender (M, F, O, N)
        cpf: Brazilian CPF number (unique identifier)
        email: Email address
        phone: Phone number
        address: Street address
        city: City
        state: State (UF)
        insurance: Health insurance information
        created_at: Record creation timestamp
        updated_at: Record update timestamp
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        date_of_birth: datetime,
        gender: str,
        cpf: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        insurance: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        super().__init__(id)
        self._name = name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._cpf = cpf
        self._email = email
        self._phone = phone
        self._address = address
        self._city = city
        self._state = state
        self._insurance = insurance
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def date_of_birth(self) -> datetime:
        return self._date_of_birth
    
    @property
    def gender(self) -> str:
        return self._gender
    
    @property
    def cpf(self) -> str:
        return self._cpf
    
    @property
    def email(self) -> Optional[str]:
        return self._email
    
    @property
    def phone(self) -> Optional[str]:
        return self._phone
    
    @property
    def address(self) -> Optional[str]:
        return self._address
    
    @property
    def city(self) -> Optional[str]:
        return self._city
    
    @property
    def state(self) -> Optional[str]:
        return self._state
    
    @property
    def insurance(self) -> Optional[str]:
        return self._insurance
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def calculate_age(self) -> int:
        """Calculate patient's age in years."""
        today = datetime.now()
        age = today.year - self._date_of_birth.year
        if (today.month, today.day) < (self._date_of_birth.month, self._date_of_birth.day):
            age -= 1
        return age
    
    def update_contact_info(self, email: str, phone: str):
        """Update patient's contact information."""
        self._email = email
        self._phone = phone
        self._updated_at = datetime.now()
    
    def update_address(self, address: str, city: str, state: str):
        """Update patient's address."""
        self._address = address
        self._city = city
        self._state = state
        self._updated_at = datetime.now()
    
    def update_insurance(self, insurance: str):
        """Update patient's health insurance."""
        self._insurance = insurance
        self._updated_at = datetime.now()
