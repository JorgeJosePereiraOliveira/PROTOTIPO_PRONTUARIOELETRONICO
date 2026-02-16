"""
Professional Domain Entity - Represents a healthcare professional
"""

from typing import Optional, List
from datetime import datetime
from ...__seedwork.entity import Entity


class Professional(Entity):
    """
    Represents a healthcare professional in the electronic patient record system.
    
    This entity encapsulates the core attributes and business rules
    related to healthcare professionals (doctors, nurses, etc.).
    
    Attributes:
        id: Unique identifier
        name: Full name of the professional
        license_number: Professional license number
        specialties: List of medical specialties
        crm: CRM number (Conselho Regional de Medicina)
        email: Professional email
        phone: Professional phone
        institution: Current institution/clinic
        created_at: Record creation timestamp
        updated_at: Record update timestamp
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        license_number: str,
        specialties: List[str],
        crm: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        institution: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        super().__init__(id)
        self._name = name
        self._license_number = license_number
        self._specialties = specialties
        self._crm = crm
        self._email = email
        self._phone = phone
        self._institution = institution
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def license_number(self) -> str:
        return self._license_number
    
    @property
    def specialties(self) -> List[str]:
        return self._specialties
    
    @property
    def crm(self) -> str:
        return self._crm
    
    @property
    def email(self) -> Optional[str]:
        return self._email
    
    @property
    def phone(self) -> Optional[str]:
        return self._phone
    
    @property
    def institution(self) -> Optional[str]:
        return self._institution
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def add_specialty(self, specialty: str):
        """Add a new specialty to the professional's list."""
        if specialty not in self._specialties:
            self._specialties.append(specialty)
            self._updated_at = datetime.now()
    
    def remove_specialty(self, specialty: str):
        """Remove a specialty from the professional's list."""
        if specialty in self._specialties:
            self._specialties.remove(specialty)
            self._updated_at = datetime.now()
    
    def update_institution(self, institution: str):
        """Update the professional's current institution."""
        self._institution = institution
        self._updated_at = datetime.now()
    
    def has_specialty(self, specialty: str) -> bool:
        """Check if professional has a specific specialty."""
        return specialty in self._specialties
