from ..__seedwork.entity import Entity


class SampleEntity(Entity):
    def __init__(self, id: str, name: str):
        super().__init__(id=id)
        self._name = name

    @property
    def name(self) -> str:
        return self._name
