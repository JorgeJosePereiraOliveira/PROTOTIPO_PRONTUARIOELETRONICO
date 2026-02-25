from prontuarioeletronico.src.domain.professional.professional_entity import Professional
from prontuarioeletronico.src.domain.professional.professional_repository_interface import ProfessionalRepositoryInterface
from datetime import datetime

class UpdateProfessionalUseCase:
    def __init__(self, repository: ProfessionalRepositoryInterface):
        self.repository = repository

    def execute(self, professional_id: str, update_data: dict) -> Professional:
        professional = self.repository.find_by_id(professional_id)
        if not professional:
            raise ValueError(f"Professional with ID {professional_id} not found")

        updated_professional = Professional(
            id=professional.id,
            name=update_data.get("name", professional.name),
            license_number=update_data.get("license_number", professional.license_number),
            specialties=update_data.get("specialties", professional.specialties),
            crm=update_data.get("crm", professional.crm),
            email=update_data.get("email", professional.email),
            phone=update_data.get("phone", professional.phone),
            institution=update_data.get("institution", professional.institution),
            created_at=professional.created_at,
            updated_at=datetime.now(),
        )

        self.repository.update(updated_professional)
        return updated_professional
