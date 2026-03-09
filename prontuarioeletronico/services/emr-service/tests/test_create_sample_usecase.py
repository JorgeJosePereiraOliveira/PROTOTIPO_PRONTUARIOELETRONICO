from src.emr.application.sample.create_sample_usecase import (
    CreateSampleInputDTO,
    CreateSampleUseCase,
)
from src.emr.infra.sample.in_memory_sample_repository import (
    InMemorySampleRepository,
)


def test_create_sample_usecase_success():
    repository = InMemorySampleRepository()
    use_case = CreateSampleUseCase(repository)

    output = use_case.execute(CreateSampleInputDTO(name="example"))

    assert output.id
    assert output.message == "sample entity created successfully"
    assert len(repository.find_all()) == 1


def test_create_sample_usecase_rejects_short_name():
    repository = InMemorySampleRepository()
    use_case = CreateSampleUseCase(repository)

    try:
        use_case.execute(CreateSampleInputDTO(name="ab"))
        assert False, "expected ValueError"
    except ValueError as error:
        assert "at least 3 characters" in str(error)
