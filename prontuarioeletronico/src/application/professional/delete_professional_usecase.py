from prontuarioeletronico.src.domain.professional.professional_repository_interface import ProfessionalRepositoryInterface

class DeleteProfessionalUseCase:
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self.repository = repository

    def execute(self, professional_id: str) -> None:
        self.repository.delete(professional_id)
