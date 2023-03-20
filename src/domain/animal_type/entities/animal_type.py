from __future__ import annotations

from dataclasses import dataclass, fields

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter

from src.domain.animal_type.value_objects import AnimalTypeID, AnimalTypeName


@dataclass
class AnimalType(Entity, EntityMerge):
    id: AnimalTypeID
    type: AnimalTypeName

    @staticmethod
    def create(animal_type: AnimalTypeName) -> AnimalType:
        return AnimalType(id=AnimalTypeID(None), type=animal_type)

    def update(self,
               type_id: AnimalTypeID | Empty = Empty.UNSET,
               animal_type: AnimalTypeName | Empty = Empty.UNSET) -> None:
        filtered_args = data_filter(type=animal_type, id=type_id)
        self._merge(**filtered_args)
