from dataclasses import dataclass

from src.domain.common.value_objects.base import ValueObject
from src.domain.common.exceptions.validation import InvalidID


@dataclass
class IDVO(ValueObject):
    value: int | None

    def __post_init__(self):
        if isinstance(self.value, int) and self.value <= 0:
            raise InvalidID(self.__field_name__)

    def to_id(self):
        return self.value
