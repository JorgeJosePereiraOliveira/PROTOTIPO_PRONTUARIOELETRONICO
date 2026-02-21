from prontuarioeletronico.src.domain.professional.professional_entity import Professional
from prontuarioeletronico.src.domain.professional.professional_repository_interface import ProfessionalRepositoryInterface

class UpdateProfessionalUseCase:
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self.repository = repository

    def execute(self, professional_id: str, update_data: dict) -> Professional:
        professional = self.repository.find_by_id(professional_id)
        for key, value in update_data.items():
            setattr(professional, key, value)
        self.repository.update(professional)
        return professional
