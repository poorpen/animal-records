from __future__ import annotations

from dataclasses import dataclass, fields
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

from src.domain.common.validations.text_fields_validations import enum_validation
from src.domain.common.validations.int_fields_validations import validation_of_min_allowable_int
from src.domain.common.validations.id_fields_validateons import check_valid_ids_animal_types


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
    def create(animal_types: List[int],
               weight: float,
               length: float,
               height: float,
               gender: str,
               chipping_location_id: int,
               chipper_id: int
               ) -> Animal:
        animal_types_entities = [TypeOfSpecificAnimal.create(animal_type_id=type_id) for type_id in animal_types]
        return Animal(id=None, animal_types=animal_types_entities, weight=weight, length=length, height=height,
                      gender=gender, life_status=LifeStatus.ALIVE, chipping_datetime=datetime.utcnow(),
                      chipping_location_id=chipping_location_id, chipper_id=chipper_id,
                      visited_locations=[],
                      death_datetime=None)

    def update(self,
               weight: float | Empty = Empty.UNSET,
               length: float | Empty = Empty.UNSET,
               height: float | Empty = Empty.UNSET,
               gender: str | Empty = Empty.UNSET,
               life_status: str | Empty = Empty.UNSET,
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

    def check_duplicate_types(self) -> TypeOfSpecificAnimal:
        for type_of_this_animal in self.animal_types:
            if self.animal_types.count(type_of_this_animal) > 1:
                return type_of_this_animal

    def check_exist_animal_type(self, animal_type_id: int) -> bool:
        for animal_type in self.animal_types:
            if animal_type.animal_type_id == animal_type_id:
                return True
        return False

    def get_animal_type(self, animal_type_id):
        validation_of_min_allowable_int(animal_type_id, 'animal_type_id', 0, '<=')
        for animal_type in self.animal_types:
            if animal_type.animal_type_id == animal_type_id:
                return animal_type
        raise AnimalNotHaveThisType(animal_id=self.id, type_id=animal_type_id)

    def get_visited_location(self, visited_location_id: int) -> AnimalVisitedLocation:
        validation_of_min_allowable_int(visited_location_id, 'visited_location_id', 0, '<=')
        for location in self.visited_locations:
            if location.id == visited_location_id:
                return location
        else:
            raise AnimalHasNoCurrentVisitedLocation(self.id, visited_location_id)

    @staticmethod
    def _validation_data(name, value):
        if name in ('weight', 'length', 'height', 'chipping_location_id', 'chipper_id'):
            validation_of_min_allowable_int(value, name, 0, '<=')
        elif name == 'gender':
            enum_validation(name, value, Gender)
        elif name == 'animal_types':
            check_valid_ids_animal_types(value, name)

    def __post_init__(self):
        for field in fields(self):
            name = field.name
            values = getattr(self, name)
            self._validation_data(name, values)
        self.gender = Gender(self.gender)

    def __post_merge__(self):
        for field in fields(self):
            name = field.name
            value = getattr(self, name)
            self._validation_data(name, value)
            if name == 'life_status':
                enum_validation(name, value, LifeStatus)
                self.life_status = LifeStatus(value)
