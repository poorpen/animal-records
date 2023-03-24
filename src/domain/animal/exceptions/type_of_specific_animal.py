from dataclasses import dataclass

from src.domain.animal_type.value_objects import AnimalTypeID
from src.domain.animal.values_objects.common import AnimalID

from src.domain.animal.exceptions.common import BaseAnimalDomainException


@dataclass
class BaseAnimalTypeException(BaseAnimalDomainException):
    animal_id: AnimalID
    type_id: AnimalTypeID


class AnimalAlreadyHaveThisType(BaseAnimalTypeException):

    def message(self):
        return f'У животного с animal_id {self.animal_id.to_id()} уже есть тип животного с type_id {self.type_id.to_id()}'


class AnimalNotHaveThisType(BaseAnimalTypeException):

    def message(self):
        return f'У животного с animal_id {self.animal_id.to_id()} нет типа животного с type_id {self.type_id.to_id()}'


class AnimalOnlyHasThisType(BaseAnimalTypeException):

    def message(self):
        return f'У животного с animal_id {self.animal_id.to_id()} только один тип и это тип с type_id {self.type_id.to_id()}'


@dataclass
class AnimalAlreadyHaveThisTypes(BaseAnimalDomainException):
    animal_id: AnimalID
    old_type: AnimalTypeID
    new_type: AnimalTypeID

    def message(self):
        return f'У животного с animal_id {self.animal_id.to_id()} уже имеются типы с ' \
               f'old_type_id {self.old_type.to_id()} и new_type_id {self.new_type.to_id()}'
