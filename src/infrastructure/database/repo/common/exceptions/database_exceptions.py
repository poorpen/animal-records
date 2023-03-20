from typing import Type

from dataclasses import dataclass

from src.domain.common.entities.entity import Entity

from src.infrastructure.database.repo.common.exceptions.base import BaseRepoException


@dataclass
class InvalidID(BaseRepoException):
    field: str

    def message(self):
        return f'Ошибка валидации: значение в поле {self.field} <= 0'


@dataclass
class LimitError(BaseRepoException):

    def message(self):
        return 'Ошибка валидации: size <= 0'


@dataclass
class OffsetError(BaseRepoException):

    def message(self):
        return 'Ошибка валидации: from < 0'


