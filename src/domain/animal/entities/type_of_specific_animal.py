from __future__ import annotations

from dataclasses import dataclass

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty


@dataclass
class TypeOfSpecificAnimal(Entity, EntityMerge):
    animal_id: int
    animal_type_id: int

    @staticmethod
    def create(animal_type_id: int,
               animal_id: int|None = None, ) -> TypeOfSpecificAnimal:
        return TypeOfSpecificAnimal(animal_id=animal_id, animal_type_id=animal_type_id)

    def update(self, animal_type_id: int):
        self._merge(animal_type_id=animal_type_id)
