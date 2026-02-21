from prontuarioeletronico.src.domain.professional.professional_entity import Professional
from prontuarioeletronico.src.domain.professional.professional_repository_interface import ProfessionalRepositoryInterface

class RegisterProfessionalUseCase:
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self.repository = repository

    def execute(self, professional_data: dict) -> Professional:
        professional = Professional(**professional_data)
        self.repository.save(professional)
        return professional
