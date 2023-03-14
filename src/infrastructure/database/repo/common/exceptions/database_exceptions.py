from typing import Type

from dataclasses import dataclass

from src.domain.common.entities.entity import Entity

from src.infrastructure.database.repo.common.exceptions.base import BaseRepoException


@dataclass
class LimitError(BaseRepoException):

    def message(self):
        return 'size <= 0'


@dataclass
class OffsetError(BaseRepoException):

    def message(self):
        return 'from < 0'
