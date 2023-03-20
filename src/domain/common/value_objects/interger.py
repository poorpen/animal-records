from dataclasses import dataclass

from src.domain.common.value_objects.base import ValueObject
from src.domain.common.exceptions.validation import IntegerMin, IntegerMax


@dataclass
class BaseIntOrFload(ValueObject):
    value: int | float
    min_value: int
    max_value: int

    def __post_init__(self):
        if self.value <= self.min_value:
            raise IntegerMin(field=self.__field_name__, min_integer=self.min_value)
        elif self.max_value and self.value >= self.max_value:
            raise IntegerMax(field=self.__field_name__, max_integer=self.min_value)


@dataclass
class IntegerVO(BaseIntOrFload):

    def to_int(self) -> int:
        return self.value


class FloatVO(BaseIntOrFload):

    def to_fload(self) -> float:
        return self.value
