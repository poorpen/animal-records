from dataclasses import dataclass

from src.domain.common.exceptions.domain import DomainException


@dataclass
class BaseAnimalTypeException(DomainException):
    animal_id: int
    type_id: int


class AnimalAlreadyHaveThisType(BaseAnimalTypeException):

    def message(self):
        return f'У животного с animal_id {self.animal_id} уже есть тип животного с type_id {self.type_id}'


class AnimalNotHaveThisType(BaseAnimalTypeException):

    def message(self):
        return f'У животного с animal_id {self.animal_id} нет типа животного с type_id {self.type_id}'


class AnimalOnlyHasThisType(BaseAnimalTypeException):

    def message(self):
        return f'У животного с animal_id {self.animal_id} только один тип и это тип с type_id {self.type_id}'


@dataclass
class AnimalAlreadyHaveThisTypes(DomainException):
    animal_id: int
    old_type: int
    new_type: int

    def message(self):
        return f'У животного с animal_id {self.animal_id} уже имеются типы с ' \
               f'old_type_id {self.old_type} и new_type_id {self.new_type}'