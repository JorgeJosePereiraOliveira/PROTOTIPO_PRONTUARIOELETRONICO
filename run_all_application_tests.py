import subprocess
import sys

TESTS = [
    'prontuarioeletronico/src/application/professional/test_professional_usecases.py',
    'prontuarioeletronico/src/application/appointment/test_appointment_usecase.py',
    'prontuarioeletronico/src/application/clinical_record/test_clinical_record_usecase.py',
    'prontuarioeletronico/src/application/patient/test_patient_usecase.py',
]

success = True
for test in TESTS:
    print(f'\nRunning {test}...')
    result = subprocess.run([sys.executable, test])
    if result.returncode != 0:
        print(f'FAILED: {test}')
        success = False
    else:
        print(f'PASSED: {test}')

if not success:
    sys.exit(1)
else:
    print('\nAll tests passed!')
