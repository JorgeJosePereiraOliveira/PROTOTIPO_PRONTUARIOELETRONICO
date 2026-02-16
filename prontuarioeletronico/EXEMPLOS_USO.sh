"""
EXEMPLOS DE USO DA API - Prontuário Eletrônico
Exemplos de requisições cURL para testar os endpoints
"""

# 1. REGISTRAR PACIENTE
# =====================

curl -X POST http://localhost:8000/api/v1/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "date_of_birth": "1990-05-15T00:00:00",
    "gender": "M",
    "cpf": "12345678901",
    "email": "joao@example.com",
    "phone": "11999999999",
    "address": "Rua A, 123",
    "city": "São Paulo",
    "state": "SP",
    "insurance": "Unimed"
  }'

# Esperado: 
# {
#   "patient_id": "uuid-xxxx",
#   "message": "Patient João Silva registered successfully"
# }


# 2. CONSULTAR PACIENTE
# =====================

curl -X GET http://localhost:8000/api/v1/patients/patient-123

# Esperado:
# {
#   "id": "patient-123",
#   "name": "João Silva",
#   "cpf": "12345678901",
#   "email": "joao@example.com",
#   "phone": "11999999999",
#   "age": 34
# }


# 3. LISTAR TODOS OS PACIENTES
# ============================

curl -X GET http://localhost:8000/api/v1/patients/

# Esperado:
# {
#   "total": 1,
#   "patients": [
#     {
#       "id": "patient-123",
#       "name": "João Silva",
#       "cpf": "12345678901"
#     }
#   ]
# }


# 4. CRIAR PROBLEMA CLÍNICO (RCOP)
# =================================

curl -X POST http://localhost:8000/api/v1/clinical-records/problems \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient-123",
    "description": "Hipertensão arterial sistêmica",
    "icd10_code": "I10"
  }'

# Esperado:
# {
#   "problem_id": "uuid-yyyy",
#   "message": "Problem created successfully: Hipertensão arterial sistêmica"
# }


# 5. REGISTRAR ENCONTRO CLÍNICO COM SOAP
# ========================================

curl -X POST http://localhost:8000/api/v1/clinical-records/soap \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient-123",
    "professional_id": "prof-456",
    "problem_id": "problem-789",
    "encounter_date": "2024-02-13T14:30:00",
    "patient_complaint": "Pressão arterial elevada mesmo com medicação",
    "vital_signs": "PA: 150/95 mmHg, FC: 72 bpm, FR: 16 irpm, Temp: 36.5°C",
    "physical_examination": "Sem alterações significativas no exame físico geral. Ausculta cardiopulmonar normal",
    "diagnosis": "Hipertensão arterial não controlada",
    "treatment_plan": "Aumentar dose de losartana de 50mg para 100mg ao dia. Reavaliação em 2 semanas",
    "medical_history": "Hipertensão desde 2015, diabetes tipo 2",
    "medications": "Losartana 50mg, Metformina 850mg",
    "allergies": "Penicilina",
    "clinical_impression": "Necessário ajuste de medicação para melhor controle pressórico"
  }'

# Esperado:
# {
#   "clinical_record_id": "uuid-zzzz",
#   "message": "SOAP clinical record registered successfully"
# }


# 6. FLUXO COMPLETO (Integrado)
# ==============================

# Step 1: Registrar paciente
PATIENT_ID=$(curl -s -X POST http://localhost:8000/api/v1/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Santos",
    "date_of_birth": "1985-03-20T00:00:00",
    "gender": "F",
    "cpf": "98765432109",
    "email": "maria@example.com"
  }' | jq -r '.patient_id')

echo "Paciente criado: $PATIENT_ID"

# Step 2: Criar problema clínico
PROBLEM_ID=$(curl -s -X POST http://localhost:8000/api/v1/clinical-records/problems \
  -H "Content-Type: application/json" \
  -d "{
    \"patient_id\": \"$PATIENT_ID\",
    \"description\": \"Diabetes Mellitus tipo 2\",
    \"icd10_code\": \"E11\"
  }" | jq -r '.problem_id')

echo "Problema criado: $PROBLEM_ID"

# Step 3: Registrar SOAP
RECORD_ID=$(curl -s -X POST http://localhost:8000/api/v1/clinical-records/soap \
  -H "Content-Type: application/json" \
  -d "{
    \"patient_id\": \"$PATIENT_ID\",
    \"professional_id\": \"prof-001\",
    \"problem_id\": \"$PROBLEM_ID\",
    \"encounter_date\": \"2024-02-13T10:30:00\",
    \"patient_complaint\": \"Glicemia elevada\",
    \"vital_signs\": \"PA: 130/80, Glicemia capilar: 280 mg/dL\",
    \"physical_examination\": \"Sem alterações\",
    \"diagnosis\": \"Diabetes descompensada\",
    \"treatment_plan\": \"Aumentar metformina e orientações dietéticas\"
  }" | jq -r '.clinical_record_id')

echo "Registro clínico criado: $RECORD_ID"
echo ""
echo "Fluxo completo executado com sucesso!"


# TESTES DE ERRO
# ==============

# Tentar registrar paciente sem nome (deve falhar)
echo ""
echo "Testando validação - registrar paciente sem nome:"
curl -X POST http://localhost:8000/api/v1/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "date_of_birth": "1990-05-15T00:00:00",
    "gender": "M",
    "cpf": "12345678901"
  }'

# Espera erro 400 ou validação
