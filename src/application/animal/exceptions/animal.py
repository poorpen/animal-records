from dataclasses import dataclass

from src.application.animal.exceptions.common import BaseAnimalException


@dataclass
class AnimalNotFound(BaseAnimalException):
    animal_id: int

    def message(self):
        return f'Животное с таким animal_id {self.animal_id} не найдено'


@dataclass
class AnimalHaveDuplicateTypes(BaseAnimalException):
    type_id: int

    def message(self):
        return f'У животное имеются дубликаты типа с type_id {self.type_id}'


@dataclass
class AnimalHaveVisitedLocation(BaseAnimalException):
    animal_id: int

    def message(self):
        return f'Животное с animal_id {self.animal_id} покинула точку чипирования и имеет другие посещенные точки '
