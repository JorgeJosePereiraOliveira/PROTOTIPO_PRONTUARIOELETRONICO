import unittest
from prontuarioeletronico.src.application.clinical_record.create_problem_usecase import CreateProblemUseCase, CreateProblemDTO
from prontuarioeletronico.src.domain.clinical_record.rcop_soap import Problem

class FakeProblemRepository:
    def __init__(self):
        self.data = {}
    def save(self, problem):
        self.data[problem.id] = problem
    def add(self, problem):
        self.save(problem)
    def update(self, problem):
        self.data[problem.id] = problem
    def find_by_id(self, problem_id):
        return self.data.get(problem_id)
    def delete(self, problem_id):
        self.data.pop(problem_id, None)

class TestCreateProblemUseCase(unittest.TestCase):
    def setUp(self):
        self.repo = FakeProblemRepository()
        self.dto = CreateProblemDTO(
            patient_id='p1',
            description='Hipertensão arterial',
            icd10_code='I10'
        )
    def test_create_problem(self):
        usecase = CreateProblemUseCase(self.repo)
        usecase._generate_id = lambda: 'prob1'
        usecase._validate_input = lambda x: None
        output = usecase.execute(self.dto)
        self.assertEqual(output.problem_id, 'prob1')
        self.assertEqual(self.repo.data['prob1'].description, 'Hipertensão arterial')

if __name__ == '__main__':
    unittest.main()
