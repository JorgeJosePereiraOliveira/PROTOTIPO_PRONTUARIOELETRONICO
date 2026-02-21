from fastapi import APIRouter, HTTPException
from prontuarioeletronico.src.application.professional.register_professional_usecase import RegisterProfessionalUseCase
from prontuarioeletronico.src.application.professional.update_professional_usecase import UpdateProfessionalUseCase
from prontuarioeletronico.src.application.professional.find_professional_usecase import FindProfessionalUseCase
from prontuarioeletronico.src.application.professional.delete_professional_usecase import DeleteProfessionalUseCase
from prontuarioeletronico.src.domain.professional.professional_repository_interface import ProfessionalRepositoryInterface

router = APIRouter()

# Instância do repositório (substitua por implementação real)
repository = ProfessionalRepositoryInterface()

@router.post("/professional")
def register_professional(professional_data: dict):
    usecase = RegisterProfessionalUseCase(repository)
    professional = usecase.execute(professional_data)
    return professional

@router.put("/professional/{professional_id}")
def update_professional(professional_id: str, update_data: dict):
    usecase = UpdateProfessionalUseCase(repository)
    professional = usecase.execute(professional_id, update_data)
    return professional

@router.get("/professional/{professional_id}")
def find_professional(professional_id: str):
    usecase = FindProfessionalUseCase(repository)
    professional = usecase.execute(professional_id)
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    return professional

@router.delete("/professional/{professional_id}")
def delete_professional(professional_id: str):
    usecase = DeleteProfessionalUseCase(repository)
    usecase.execute(professional_id)
    return {"detail": "Professional deleted"}
