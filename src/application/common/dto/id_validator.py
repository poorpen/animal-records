from dataclasses import dataclass

from src.application.common.exceptions.identifier import InvalidID


@dataclass
class IDValidator:

    def __post_init__(self):
        if self.id <= 0:
            raise InvalidID('id')
