from prontuarioeletronico.src.domain.professional.professional_entity import Professional
from prontuarioeletronico.src.domain.professional.professional_repository_interface import ProfessionalRepositoryInterface

class UpdateProfessionalUseCase:
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self.repository = repository

    def execute(self, professional_id: str, update_data: dict) -> Professional:
        professional = self.repository.find_by_id(professional_id)
        # Atualize apenas campos permitidos via métodos do domínio
        if 'institution' in update_data:
            professional.update_institution(update_data['institution'])
        if 'email' in update_data:
            professional._email = update_data['email']  # Se permitido
        if 'phone' in update_data:
            professional._phone = update_data['phone']  # Se permitido
        if 'crm' in update_data:
            professional._crm = update_data['crm']  # Se permitido
        # Adicione lógica para specialties se necessário
        self.repository.update(professional)
        return professional
