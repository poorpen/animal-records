from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge
from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter

from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal

from src.domain.animal.value_objects.gender import Gender
from src.domain.animal.value_objects.life_status import LifeStatus

from src.domain.animal.exceptions.animal_visited_location import AnimalHasNoCurrentVisitedLocation

from src.domain.animal.exceptions.type_of_specific_animal import AnimalNotHaveThisType


@dataclass
class Animal(Entity, EntityMerge):
    id: int
    animal_types: List[TypeOfSpecificAnimal]
    weight: float
    length: float
    height: float
    gender: Gender
    life_status: LifeStatus
    chipping_datetime: datetime
    chipping_location_id: int
    chipper_id: int
    visited_locations: List[AnimalVisitedLocation]
    death_datetime: None | datetime

    @staticmethod
    def create(animal_types: List[TypeOfSpecificAnimal],
               weight: float,
               length: float,
               height: float,
               gender: Gender,
               chipping_location_id: int,
               chipper_id: int,
               life_status: LifeStatus | None = None,
               chipping_datetime: datetime | None = None,
               animal_id: int | None = None,
               visited_locations: List[AnimalVisitedLocation] | None = None,
               death_datetime: datetime | None = None,
               ) -> Animal:

        return Animal(id=animal_id, animal_types=animal_types, weight=weight, length=length, height=height,
                      gender=gender, life_status=life_status, chipping_datetime=chipping_datetime,
                      chipping_location_id=chipping_location_id, chipper_id=chipper_id,
                      visited_locations=visited_locations if visited_locations else [],
                      death_datetime=death_datetime)

    def update(self,
               weight: float | Empty = Empty.UNSET,
               length: float | Empty = Empty.UNSET,
               height: float | Empty = Empty.UNSET,
               gender: Gender | Empty = Empty.UNSET,
               life_status: LifeStatus | Empty = Empty.UNSET,
               chipper_id: int | Empty = Empty.UNSET,
               chipping_location_id: int | Empty = Empty.UNSET,
               animal_types: List[TypeOfSpecificAnimal] | Empty = Empty.UNSET,
               visited_locations: List[AnimalVisitedLocation] | Empty = Empty.UNSET
               ) -> None:
        filtered_args = data_filter(weight=weight, length=length, height=height, gender=gender, life_status=life_status,
                                    chipper=chipper_id, chipping_location=chipping_location_id,
                                    animal_types=animal_types,
                                    visited_locations=visited_locations)
        self._merge(**filtered_args)

    def set_death_datetime(self) -> None:
        if self.life_status == LifeStatus.DEAD:
            self.death_datetime = datetime.utcnow()

    def get_animal_type(self, animal_type_id):
        for animal_type in self.animal_types:
            if animal_type.animal_type_id == animal_type_id:
                return animal_type
        raise AnimalNotHaveThisType(animal_id=self.id, type_id=animal_type_id)

    def check_duplicate_types(self) -> TypeOfSpecificAnimal:
        for type_of_this_animal in self.animal_types:
            if self.animal_types.count(type_of_this_animal) > 1:
                return type_of_this_animal

    def check_exist_animal_type(self, animal_type_id: int) -> bool:
        for animal_type in self.animal_types:
            if animal_type.animal_type_id == animal_type_id:
                return True
        return False

    def get_visited_location(self, visited_location_id: int) -> AnimalVisitedLocation:
        for location in self.visited_locations:
            if location.id == visited_location_id:
                return location
        else:
            raise AnimalHasNoCurrentVisitedLocation(self.id, visited_location_id)
