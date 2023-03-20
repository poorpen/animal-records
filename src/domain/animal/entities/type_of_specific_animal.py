from __future__ import annotations

from dataclasses import dataclass

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter

from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.values_objects.type_of_specific_animal import AnimalTypeID


@dataclass
class TypeOfSpecificAnimal(Entity, EntityMerge):
    animal_type_id: AnimalTypeID
    animal_id: AnimalID

    @staticmethod
    def create(animal_type_id: AnimalTypeID) -> TypeOfSpecificAnimal:
        return TypeOfSpecificAnimal(animal_id=AnimalID(None), animal_type_id=animal_type_id)

    def update(self,
               animal_id: AnimalTypeID | Empty = Empty.UNSET,
               animal_type_id: AnimalTypeID | Empty = Empty.UNSET):
        filtered_args = data_filter(animal_id=animal_id, animal_type_id=animal_type_id)
        self._merge(**filtered_args)
