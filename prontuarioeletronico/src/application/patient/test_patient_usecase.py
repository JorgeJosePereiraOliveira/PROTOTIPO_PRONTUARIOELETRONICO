import unittest
from datetime import datetime
from prontuarioeletronico.src.application.patient.register_patient_usecase import RegisterPatientUseCase, RegisterPatientDTO
from prontuarioeletronico.src.domain.patient.patient_entity import Patient

class FakePatientRepository:
    def __init__(self):
        self.data = {}
    def save(self, patient):
        self.data[patient.id] = patient
    def add(self, patient):
        self.save(patient)
    def update(self, patient):
        self.data[patient.id] = patient
    def find_by_id(self, patient_id):
        return self.data.get(patient_id)
    def delete(self, patient_id):
        self.data.pop(patient_id, None)

class TestRegisterPatientUseCase(unittest.TestCase):
    def setUp(self):
        self.repo = FakePatientRepository()
        self.dto = RegisterPatientDTO(
            name='Paciente Teste',
            date_of_birth=datetime(1990, 1, 1),
            gender='M',
            cpf='12345678900',
            email='paciente@teste.com',
            phone='999999999',
            address='Rua X',
            city='Cidade Y',
            state='UF',
            insurance='Plano Z'
        )
    def test_register_patient(self):
        usecase = RegisterPatientUseCase(self.repo)
        usecase._generate_id = lambda: 'pat1'
        usecase._validate_input = lambda x: None
        output = usecase.execute(self.dto)
        self.assertEqual(output.patient_id, 'pat1')
        self.assertEqual(self.repo.data['pat1'].name, 'Paciente Teste')

if __name__ == '__main__':
    unittest.main()
