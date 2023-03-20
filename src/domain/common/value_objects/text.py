from dataclasses import dataclass

from src.domain.common.exceptions.validation import EmptyField
from src.domain.common.value_objects.base import ValueObject


@dataclass
class TextVO(ValueObject):
    value: str

    def __post_init__(self):
        if not self.value or self.value.isspace():
            raise EmptyField(self.__field_name__)

    def to_string(self) -> str:
        return self.value
