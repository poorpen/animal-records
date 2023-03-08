from typing import List
from datetime import datetime
from dataclasses import dataclass

from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.value_objects.gender import Gender

from src.application.common.dto.base import DTO


@dataclass
class BaseAnimalDTO(DTO):
    chipper_id: int
    chipping_location_id: int
    life_status: LifeStatus
    gender: Gender


@dataclass
class SearchParametersDTO(BaseAnimalDTO):
    start_datetime: datetime
    end_datetime: datetime
    limit: int
    offset: int


@dataclass
class BaseAnimalDTO(BaseAnimalDTO):
    weight: float
    length: float
    height: float


@dataclass
class CreateAnimalDTO(BaseAnimalDTO):
    animal_types: List[int]
    life_status: LifeStatus


@dataclass
class UpdateAnimalDTO(BaseAnimalDTO):
    id: int


class AnimalDTO(BaseAnimalDTO):
    id: int
    animal_types: List[int]
    chipping_datetime: datetime
    visited_location: List[int]
    death_datetime: datetime
