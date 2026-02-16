"""
Use Case: Create/Register a new clinical problem
"""

from ...domain.__seedwork.use_case_interface import UseCase
from ...domain.clinical_record.rcop_soap import Problem


class CreateProblemDTO:
    """Data Transfer Object for creating a problem"""
    
    def __init__(
        self,
        patient_id: str,
        description: str,
        icd10_code: str = None
    ):
        self.patient_id = patient_id
        self.description = description
        self.icd10_code = icd10_code


class CreateProblemOutputDTO:
    """Data Transfer Object for problem creation output"""
    
    def __init__(self, problem_id: str, message: str):
        self.problem_id = problem_id
        self.message = message


class CreateProblemUseCase(UseCase[CreateProblemDTO, CreateProblemOutputDTO]):
    """
    Use Case for creating a new clinical problem in the RCOP system.
    
    This use case handles the registration of a new health problem
    that will be tracked and monitored through SOAP notes.
    """
    
    def __init__(self, problem_repository):
        self._repository = problem_repository
    
    def execute(self, input_dto: CreateProblemDTO) -> CreateProblemOutputDTO:
        """
        Execute the use case to create a new problem.
        
        Args:
            input_dto: Input data for the new problem
            
        Returns:
            CreateProblemOutputDTO: Result with the created problem ID
        """
        # Validate input
        self._validate_input(input_dto)
        
        # Create the problem entity
        problem = Problem(
            id=self._generate_id(),
            patient_id=input_dto.patient_id,
            description=input_dto.description,
            icd10_code=input_dto.icd10_code,
            status="active"
        )
        
        # Persist the problem
        self._repository.add(problem)
        
        return CreateProblemOutputDTO(
            problem_id=problem.id,
            message=f"Problem created successfully: {problem.description}"
        )
    
    def _validate_input(self, input_dto: CreateProblemDTO):
        """Validate input according to business rules"""
        if not input_dto.patient_id:
            raise ValueError("Patient ID is required")
        if not input_dto.description or len(input_dto.description) < 3:
            raise ValueError("Problem description is required and must be at least 3 characters")
    
    def _generate_id(self) -> str:
        """Generate a unique ID"""
        import uuid
        return str(uuid.uuid4())
