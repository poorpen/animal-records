from __future__ import annotations

from dataclasses import dataclass, fields

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter

from src.domain.common.validations.text_fields_validations import text_field_validation


@dataclass
class AnimalType(Entity, EntityMerge):
    id: int
    type: str

    @staticmethod
    def create(animal_type: str,
               type_id: int | None = None
               ) -> AnimalType:
        return AnimalType(id=type_id, type=animal_type)

    def update(self, animal_type: str | Empty = Empty.UNSET) -> None:
        filtered_args = data_filter(type=animal_type)
        self._merge(**filtered_args)

    def __post_init__(self):
        field = fields(self)[-1]
        values = getattr(self, field.name)
        text_field_validation(field.name, values)

    def __post_merge__(self):
        field = fields(self)[-1]
        values = getattr(self, field.name)
        text_field_validation(field.name, values)
