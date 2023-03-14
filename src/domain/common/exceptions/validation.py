from dataclasses import dataclass

from src.domain.common.exceptions.domain import DomainException


@dataclass
class BaseModelException(DomainException):
    field: str


@dataclass
class NoneField(BaseModelException):

    def message(self):
        return f'Ошибка валидации: поле {self.field} = null'


@dataclass
class EmptyField(BaseModelException):

    def message(self):
        return f'Ошибка валидации: значение в поле {self.field} является пустой строкой, или состоит из пробелов'


@dataclass
class IntegerMin(BaseModelException):
    min_integer: int

    def message(self):
        return f'Ошибка валидации: значение/я в поле {self.field} меньше или равно {self.min_integer}'


@dataclass
class IntegerMax(BaseModelException):
    max_integer: int

    def message(self):
        return f'Ошибка валидации: значение в поле {self.field} больше или равно {self.max_integer}'


@dataclass
class EmailValidationError(BaseModelException):
    email: str

    def message(self):
        return f'Ошибка валидации: email {self.email} в поле {self.field} невалиден'


@dataclass
class EnumError(BaseModelException):
    value: str
    expected_values: list[str]

    def message(self):
        return f'Ошибка валидации: передано значение {self.value} выходящее за рамки ожидаемых {self.expected_values}'


class ListEmpty(BaseModelException):

    def message(self):
        return f'Ошибка валидации: список {self.field} пустой'


