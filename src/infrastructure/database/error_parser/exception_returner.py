from typing import Callable

from src.domain.common.entities.entity import Entity


class ExceptionReturner:

    def __init__(self, func: Callable, database_column: str):
        self.func = func
        self.database_column = database_column

    def check(self, expected_database_column):
        if self.database_column == expected_database_column:
            return True
        return False

    def return_exception(self, exception_value):
        return self.func(exception_value)
