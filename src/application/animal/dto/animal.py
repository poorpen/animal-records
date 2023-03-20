from typing import List
from datetime import datetime
from dataclasses import dataclass

from src.domain.animal.enums import LifeStatus

from src.application.common.dto.base import DTO


@dataclass
class BaseAnimalDTO(DTO):
    chipper_id: int
    chipping_location_id: int
    gender: str


@dataclass
class SearchParametersDTO(BaseAnimalDTO):
    life_status: LifeStatus
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


@dataclass
class UpdateAnimalDTO(BaseAnimalDTO):
    id: int
    life_status: str



@dataclass
class AnimalDTO(BaseAnimalDTO):
    id: int
    animal_types: List[int]
    life_status: LifeStatus
    chipping_datetime: datetime
    visited_locations: List[int]
    death_datetime: datetime


@dataclass
class AnimalDTOs(DTO):
    animals: List[AnimalDTO]
