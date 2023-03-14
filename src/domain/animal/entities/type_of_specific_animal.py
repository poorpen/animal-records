from __future__ import annotations

from dataclasses import dataclass, fields

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.validations.int_fields_validations import validation_of_min_allowable_int


@dataclass
class TypeOfSpecificAnimal(Entity, EntityMerge):
    animal_type_id: int

    @staticmethod
    def create(animal_type_id: int) -> TypeOfSpecificAnimal:
        return TypeOfSpecificAnimal(animal_type_id=animal_type_id)

    def update(self, animal_type_id: int):
        self._merge(animal_type_id=animal_type_id)

    def __post_init__(self):
        name = 'animal_type_id'
        animal_type = getattr(self, name)
        validation_of_min_allowable_int(animal_type, name, 0, '<=')

    def __post_merge__(self):
        name = 'animal_type_id'
        animal_type = getattr(self, name)
        validation_of_min_allowable_int(animal_type, name, 0, '<=')
