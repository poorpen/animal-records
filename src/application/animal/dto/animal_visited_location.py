from typing import List

from dataclasses import dataclass
from datetime import datetime

from src.application.common.dto.base import DTO
from src.application.common.dto.id_validator import IDValidator
from src.application.animal.dto.common import ValidateAnimalID


@dataclass
class SearchParametersDTO(ValidateAnimalID, DTO):
    animal_id: int
    start_datetime: datetime
    end_datetime: datetime
    limit: int
    offset: int


@dataclass
class AddAnimalVisitedLocationDTO(ValidateAnimalID, DTO):
    location_point_id: int


@dataclass
class ChangeAnimalVisitedLocationDTO(ValidateAnimalID, IDValidator, DTO):
    id: int
    animal_id: int
    location_point_id: int

    def __post_init__(self):
        ValidateAnimalID.__post_init__(self)
        IDValidator.__post_init__(self)


@dataclass
class AnimalVisitedLocationDTO(DTO):
    id: int
    datetime_of_visit: datetime
    location_point_id: int


@dataclass
class AnimalVisitedLocationDTOs(DTO):
    visited_locations: List[AnimalVisitedLocationDTO]
