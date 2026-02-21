import unittest
from prontuarioeletronico.src.application.professional.register_professional_usecase import RegisterProfessionalUseCase
from prontuarioeletronico.src.application.professional.update_professional_usecase import UpdateProfessionalUseCase
from prontuarioeletronico.src.application.professional.find_professional_usecase import FindProfessionalUseCase
from prontuarioeletronico.src.application.professional.delete_professional_usecase import DeleteProfessionalUseCase
from prontuarioeletronico.src.domain.professional.professional_entity import Professional

class FakeProfessionalRepository:
    def __init__(self):
        self.data = {}
    def save(self, professional):
        self.data[professional.id] = professional
    def update(self, professional):
        self.data[professional.id] = professional
    def find_by_id(self, professional_id):
        return self.data.get(professional_id)
    def delete(self, professional_id):
        self.data.pop(professional_id, None)

class TestProfessionalUseCases(unittest.TestCase):
    def setUp(self):
        self.repo = FakeProfessionalRepository()
        self.professional_data = {'id': '1', 'name': 'Dr. Test'}
    def test_register_professional(self):
        usecase = RegisterProfessionalUseCase(self.repo)
        professional = usecase.execute(self.professional_data)
        self.assertEqual(professional.name, 'Dr. Test')
    def test_update_professional(self):
        usecase = RegisterProfessionalUseCase(self.repo)
        professional = usecase.execute(self.professional_data)
        update_usecase = UpdateProfessionalUseCase(self.repo)
        updated = update_usecase.execute('1', {'name': 'Dr. Updated'})
        self.assertEqual(updated.name, 'Dr. Updated')
    def test_find_professional(self):
        usecase = RegisterProfessionalUseCase(self.repo)
        professional = usecase.execute(self.professional_data)
        find_usecase = FindProfessionalUseCase(self.repo)
        found = find_usecase.execute('1')
        self.assertEqual(found.name, 'Dr. Test')
    def test_delete_professional(self):
        usecase = RegisterProfessionalUseCase(self.repo)
        professional = usecase.execute(self.professional_data)
        delete_usecase = DeleteProfessionalUseCase(self.repo)
        delete_usecase.execute('1')
        self.assertIsNone(self.repo.find_by_id('1'))

if __name__ == '__main__':
    unittest.main()
