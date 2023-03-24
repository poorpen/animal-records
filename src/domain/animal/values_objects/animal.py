from dataclasses import dataclass

from src.domain.common.exceptions.validation import EnumError
from src.domain.common.value_objects.base import ValueObject
from src.domain.common.value_objects.id import IDVO
from src.domain.common.value_objects.integer import FloatVO

from src.domain.animal.enums import LifeStatus, Gender


class ValidateEnum:

    def __post_init__(self):
        expected_values = [row.value for row in self.expected_enum]
        if self.value not in expected_values:
            raise EnumError(field=self.__field_name__, expected_values=expected_values, value=self.value)


class AnimalParam(FloatVO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, min_value=0, max_value=None)


class Weight(AnimalParam):
    __field_name__ = 'weight'


class Length(AnimalParam):
    __field_name__ = 'length'


class Height(AnimalParam):
    __field_name__ = 'height'


@dataclass
class GenderVO(ValueObject, ValidateEnum):
    __field_name__ = 'gender'
    expected_enum = Gender
    value: str

    def to_enum(self):
        return self.expected_enum(self.value)


@dataclass
class LifeStatusVO(ValueObject, ValidateEnum):
    __field_name__ = 'life_status'
    expected_enum = LifeStatus
    value: str

    def to_enum(self):
        return self.expected_enum(self.value)


class ChippingLocationID(IDVO):
    __field_name__ = 'chipping_location_id'


class ChipperID(IDVO):
    __field_name__ = 'chipper_id'

