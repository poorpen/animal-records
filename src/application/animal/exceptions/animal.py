from dataclasses import dataclass

from src.application.common.exceptions.application import ApplicationException


@dataclass
class AnimalNotFound(ApplicationException):
    animal_id: int

    def message(self):
        return f'Животное с таким animal_id {self.animal_id} не найдено'


@dataclass
class AnimalHaveDuplicateTypes(ApplicationException):
    type_id: int

    def message(self):
        return f'У животное имеются дубликаты типа с type_id {self.type_id}'


@dataclass
class AnimalHaveVisitedLocation(AnimalHaveDuplicateTypes):
    animal_id: int

    def message(self):
        return f'Животное с animal_id {self.animal_id} покинула точку чипирования и имеет другие посещенные точки '
