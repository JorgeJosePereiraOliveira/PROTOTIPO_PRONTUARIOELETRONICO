from prontuarioeletronico.src.domain.professional.professional_repository_interface import ProfessionalRepositoryInterface
from prontuarioeletronico.src.domain.professional.professional_entity import Professional

class FindProfessionalUseCase:
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self.repository = repository

    def execute(self, professional_id: str) -> Professional:
        return self.repository.find_by_id(professional_id)
