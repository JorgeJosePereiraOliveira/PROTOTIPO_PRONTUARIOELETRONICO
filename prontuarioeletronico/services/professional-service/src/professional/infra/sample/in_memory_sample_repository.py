from ...domain.sample.sample_entity import SampleEntity
from ...domain.sample.sample_repository_interface import SampleRepositoryInterface


class InMemorySampleRepository(SampleRepositoryInterface):
    def __init__(self):
        self._data: dict[str, SampleEntity] = {}

    def add(self, entity: SampleEntity) -> None:
        self._data[entity.id] = entity

    def update(self, entity: SampleEntity) -> None:
        self._data[entity.id] = entity

    def delete(self, id: str) -> None:
        self._data.pop(id, None)

    def find_by_id(self, id: str):
        return self._data.get(id)

    def find_all(self):
        return list(self._data.values())
