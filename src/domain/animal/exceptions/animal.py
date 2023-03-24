from dataclasses import dataclass

from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.values_objects.animal import ChippingLocationID

from src.domain.animal.exceptions.common import BaseAnimalDomainException


@dataclass
class AnimalIsDead(BaseAnimalDomainException):
    animal_id: AnimalID

    def message(self):
        return f'У животного с animal_id {self.animal_id.to_id()} life_status = "DEAD"'


@dataclass
class AttemptToResurrectAnimal(BaseAnimalDomainException):
    animal_id: AnimalID

    def message(self):
        return f'Попытка изменить у животного с animal_id {self.animal_id.to_id()} статус с "DEAD" на "ALIVE"'


@dataclass
class ChippingLocationEqualFirstLocation(BaseAnimalDomainException):
    animal_id: AnimalID
    chipping_location: ChippingLocationID

    def message(self):
        return f'Новая точка чипирования c location_id {self.chipping_location.to_id()} у животного с animal_id' \
               f' {self.animal_id.to_id()}' \
               f'совпадает с первой посещенной точкой'
