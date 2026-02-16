"""
Use Case: Register a new patient
"""

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.patient.patient_entity import Patient
from datetime import datetime


class RegisterPatientDTO:
    """Data Transfer Object for registering a patient"""
    
    def __init__(
        self,
        name: str,
        date_of_birth: datetime,
        gender: str,
        cpf: str,
        email: str = None,
        phone: str = None,
        address: str = None,
        city: str = None,
        state: str = None,
        insurance: str = None
    ):
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.cpf = cpf
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.insurance = insurance


class RegisterPatientOutputDTO:
    """Data Transfer Object for patient registration output"""
    
    def __init__(self, patient_id: str, message: str):
        self.patient_id = patient_id
        self.message = message


class RegisterPatientUseCase(UseCase[RegisterPatientDTO, RegisterPatientOutputDTO]):
    """
    Use Case for registering a new patient in the system.
    """
    
    def __init__(self, patient_repository):
        self._repository = patient_repository
    
    def execute(self, input_dto: RegisterPatientDTO) -> RegisterPatientOutputDTO:
        """
        Execute the use case to register a new patient.
        """
        # Validate input
        self._validate_input(input_dto)
        
        # Create patient entity
        patient = Patient(
            id=self._generate_id(),
            name=input_dto.name,
            date_of_birth=input_dto.date_of_birth,
            gender=input_dto.gender,
            cpf=input_dto.cpf,
            email=input_dto.email,
            phone=input_dto.phone,
            address=input_dto.address,
            city=input_dto.city,
            state=input_dto.state,
            insurance=input_dto.insurance
        )
        
        # Persist the patient
        self._repository.add(patient)
        
        return RegisterPatientOutputDTO(
            patient_id=patient.id,
            message=f"Patient {patient.name} registered successfully"
        )
    
    def _validate_input(self, input_dto: RegisterPatientDTO):
        """Validate input according to business rules"""
        if not input_dto.name or len(input_dto.name) < 3:
            raise ValueError("Patient name is required and must be at least 3 characters")
        if not input_dto.cpf or len(input_dto.cpf) < 11:
            raise ValueError("Valid CPF is required")
        if not input_dto.gender or input_dto.gender not in ['M', 'F', 'O', 'N']:
            raise ValueError("Gender must be one of: M, F, O, N")
    
    def _generate_id(self) -> str:
        """Generate a unique ID"""
        import uuid
        return str(uuid.uuid4())
