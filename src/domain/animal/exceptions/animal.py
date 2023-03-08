from dataclasses import dataclass

from src.domain.common.exceptions.domain import DomainException


@dataclass
class AnimalIsDead(DomainException):
    animal_id: int

    def message(self):
        return f'У животного с animal_id {self.animal_id} life_status = "DEAD"'

