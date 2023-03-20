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

from src.domain.animal.exceptions.animal_visited_location import AnimalHasNoCurrentVisitedLocation

from src.domain.animal.exceptions.type_of_specific_animal import AnimalNotHaveThisType

from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.values_objects.animal_visited_location import VisitedLocationID
from src.domain.animal.values_objects.type_of_specific_animal import AnimalTypeID
from src.domain.animal.values_objects.animal import Weight, Length, Height, GenderVO, LifeStatusVO, \
    ChippingLocationID, ChipperID


@dataclass
class Animal(Entity, EntityMerge):
    id: AnimalID
    animal_types: List[TypeOfSpecificAnimal]
    weight: Weight
    length: Length
    height: Height
    gender: GenderVO
    life_status: LifeStatusVO
    chipping_datetime: datetime
    chipping_location_id: ChippingLocationID
    chipper_id: ChipperID
    visited_locations: List[AnimalVisitedLocation]
    death_datetime: None | datetime

    @staticmethod
    def create(animal_types: List[int],
               weight: Weight,
               length: Length,
               height: Height,
               gender: GenderVO,
               chipping_location_id: ChippingLocationID,
               chipper_id: chipper_id
               ) -> Animal:
        animal_types_entities = [TypeOfSpecificAnimal.create(animal_type_id=AnimalTypeID(type_id)) for type_id in
                                 animal_types]
        return Animal(id=AnimalID(None),
                      animal_types=animal_types_entities,
                      weight=weight,
                      length=length,
                      height=height,
                      gender=gender,
                      life_status=LifeStatusVO('ALIVE'), chipping_datetime=datetime.utcnow(),
                      chipping_location_id=chipping_location_id, chipper_id=chipper_id,
                      visited_locations=[None],
                      death_datetime=None)

    def update(self,
               animal_id: AnimalID | Empty = Empty.UNSET,
               weight: Weight | Empty = Empty.UNSET,
               length: Length | Empty = Empty.UNSET,
               height: Height | Empty = Empty.UNSET,
               gender: GenderVO | Empty = Empty.UNSET,
               life_status: LifeStatusVO | Empty = Empty.UNSET,
               chipper_id: ChipperID | Empty = Empty.UNSET,
               chipping_location_id: ChippingLocationID | Empty = Empty.UNSET,
               animal_types: List[TypeOfSpecificAnimal] | Empty = Empty.UNSET,
               visited_locations: List[AnimalVisitedLocation] | Empty = Empty.UNSET
               ) -> None:
        filtered_args = data_filter(weight=weight, length=length, height=height, gender=gender, life_status=life_status,
                                    chipper=chipper_id, chipping_location=chipping_location_id,
                                    animal_types=animal_types,
                                    visited_locations=visited_locations, id=animal_id)
        self._merge(**filtered_args)

    def check_duplicate_types(self) -> TypeOfSpecificAnimal:
        for type_of_this_animal in self.animal_types:
            if self.animal_types.count(type_of_this_animal) > 1:
                return type_of_this_animal

    def check_exist_animal_type(self, animal_type_id: int) -> bool:
        for animal_type in self.animal_types:
            if animal_type.animal_type_id.to_id() == animal_type_id:
                return True
        return False

    def get_animal_type(self, animal_type_id: int):
        animal_type_vo = AnimalTypeID(animal_type_id)
        for animal_type in self.animal_types:
            if animal_type.animal_type_id == animal_type_vo:
                return animal_type
        raise AnimalNotHaveThisType(animal_id=self.id.to_id(), type_id=animal_type_id)

    def get_visited_location(self, visited_location_id: int) -> AnimalVisitedLocation:
        visited_location_vo = VisitedLocationID(visited_location_id)
        for location in self.visited_locations:
            if location.id == visited_location_vo:
                return location
        else:
            raise AnimalHasNoCurrentVisitedLocation(self.id.to_id(), visited_location_id)
