from dataclasses import dataclass

from src.application.common.dto.base import DTO
from src.application.common.dto.id_validator import IDValidator
from src.application.common.exceptions.identifier import InvalidID


@dataclass
class ValidateAnimalID(DTO):

    def __post_init__(self):
        if self.animal_id <= 0:
            raise InvalidID('animal_id')
