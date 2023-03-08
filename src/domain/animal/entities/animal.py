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
from src.domain.animal.exceptions.animal import AnimalIsDead

from src.domain.animal.exceptions.animal_visited_location import \
    LocationPointEqualToChippingLocation, AnimalHasNoCurrentVisitedLocation, NextOfPreviousEqualThisLocation, \
    UpdateToSameLocationPoint, UpdatedFirstPointToChippingPoint, AnimalNowInThisPoint

from src.domain.animal.exceptions.type_specific_animal import \
    AnimalAlreadyHaveThisType, AnimalAlreadyHaveThisTypes, AnimalNotHaveThisType, AnimalOnlyHasThisType


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
    death_datetime: Empty | datetime

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
               animal_types_ids: List[TypeOfSpecificAnimal] | Empty = Empty.UNSET,
               visited_location: List[AnimalVisitedLocation] | Empty = Empty.UNSET
               ) -> None:
        filtered_args = data_filter(weight=weight, length=length, height=height, gender=gender, life_status=life_status,
                                    chipper=chipper_id, chipping_location=chipping_location_id)
        self._merge(**filtered_args)

    def check_life_status(self) -> None:
        if self.life_status == LifeStatus.DEAD:
            self.death_datetime = datetime.utcnow()

    def check_duplicate_types(self) -> TypeOfSpecificAnimal:
        for type_of_this_animal in self.animal_types:
            if self.animal_types.count(type_of_this_animal) > 1:
                return type_of_this_animal

    def add_visited_location(self, visited_location: AnimalVisitedLocation) -> None:
        if self.life_status == LifeStatus.DEAD:
            raise AnimalIsDead(self.id)
        elif self.chipping_location_id == visited_location.location_point_id:
            raise LocationPointEqualToChippingLocation(self.id, visited_location.location_point_id)
        elif self.visited_locations[-1].location_point_id == visited_location.location_point_id:
            raise AnimalNowInThisPoint(self.id, visited_location.location_point_id)
        self.update(visited_location=[visited_location])

    def get_visited_location(self, visited_location_id: int) -> AnimalVisitedLocation:
        for location in self.visited_locations:
            if location.id == visited_location_id:
                return location
        else:
            raise AnimalHasNoCurrentVisitedLocation(self.id, visited_location_id)

    def change_visited_location(self, visited_location: AnimalVisitedLocation) -> None:
        location_index = self.visited_locations.index(visited_location)
        if self.visited_locations[location_index].location_point_id == visited_location.location_point_id:
            raise UpdateToSameLocationPoint(self.id, visited_location.location_point_id)
        elif self.visited_locations[location_index + 1].location_point_id == visited_location.location_point_id:
            raise NextOfPreviousEqualThisLocation(self.id, visited_location.location_point_id)
        elif self.visited_locations[location_index - 1].location_point_id == visited_location.location_point_id:
            raise NextOfPreviousEqualThisLocation(self.id, visited_location.location_point_id)
        elif location_index == 0 and visited_location.location_point_id == self.chipping_location_id:
            raise UpdatedFirstPointToChippingPoint(self.id, visited_location.location_point_id)
        self.visited_locations[location_index] = visited_location

    def delete_visited_location(self, visited_location_id) -> None:
        visited_location = self.get_visited_location(visited_location_id)

        index_visited_location = self.visited_locations.index(visited_location)
        next_visited_location = self.visited_locations[index_visited_location + 1]

        if index_visited_location == 0 and next_visited_location.location_point_id == self.chipping_location_id:
            self.visited_locations.remove(next_visited_location)
        self.visited_locations.remove(visited_location)

    def add_animal_type(self, type_of_this_animal: TypeOfSpecificAnimal) -> None:
        if type_of_this_animal in self.animal_types:
            raise AnimalAlreadyHaveThisType(self.id, type_of_this_animal.animal_type_id)
        self.update(animal_types_ids=[type_of_this_animal])

    def get_animal_type(self, animal_type_id):
        for animal_type in self.animal_types:
            if animal_type.animal_type_id == animal_type_id:
                return animal_type_id
        raise AnimalNotHaveThisType(self.id, animal_type_id)

    def change_animal_type(self,
                           old_type_of_this_animal: TypeOfSpecificAnimal,
                           new_type_of_this_animal: TypeOfSpecificAnimal
                           ) -> None:
        if old_type_of_this_animal in self.animal_types and new_type_of_this_animal in self.animal_types:
            raise AnimalAlreadyHaveThisTypes(self.id, old_type_of_this_animal.animal_type_id,
                                             new_type_of_this_animal.animal_type_id)
        elif new_type_of_this_animal in self.animal_types:
            raise AnimalAlreadyHaveThisType(self.id, new_type_of_this_animal.animal_type_id)

        type_index = self.animal_types.index(old_type_of_this_animal)
        self.animal_types[type_index] = new_type_of_this_animal

    def delete_animal_type(self, animal_type_id: int) -> None:
        type_of_this_animal = self.get_animal_type(animal_type_id)
        if len(self.animal_types) == 1 and self.animal_types[0] == type_of_this_animal:
            raise AnimalOnlyHasThisType(self.id, type_of_this_animal.animal_type_id)
        elif type_of_this_animal not in self.animal_types:
            raise AnimalNotHaveThisType(self.id, type_of_this_animal.animal_type_id)
        self.animal_types.remove(type_of_this_animal)
