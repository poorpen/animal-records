from typing import Callable, Type

from src.domain.common.entities.entity import Entity


class ExceptionReturner:

    def __init__(self, func: Callable, entity: Type[Entity], database_column: str):
        self._database_column = database_column
        self._entity = entity
        self.func = func

    def check(self, expected_database_column: str, entity: Type[Entity]):
        if self._database_column == expected_database_column and self._entity == entity:
            return True
        return False

    def return_exception(self, entity: Entity):
        return self.func(entity)
