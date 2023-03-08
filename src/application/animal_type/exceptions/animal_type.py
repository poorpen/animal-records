from dataclasses import dataclass

from src.application.common.exceptions.application import ApplicationException


@dataclass
class AnimalTypeNotFound(ApplicationException):
    type_id: int

    def message(self):
        return f'Тип животного с type_id {self.type_id} не найден'


@dataclass
class AnimalTypeAlreadyExist(ApplicationException):
    type: str

    def message(self):
        return f'Тип животного с таким type {self.type} уже существует'


@dataclass
class AnimalHaveType(ApplicationException):
    type_id: int

    def message(self):
        return f'Некоторые животные ссылаются на тип с type_id {self.type_id}'
