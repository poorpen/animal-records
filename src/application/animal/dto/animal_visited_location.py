from typing import List

from dataclasses import dataclass
from datetime import datetime

from src.application.common.dto.base import DTO


@dataclass
class SearchParametersDTO(DTO):
    animal_id: int
    start_datetime: datetime
    end_datetime: datetime
    limit: int
    offset: int


@dataclass
class AddAnimalVisitedLocationDTO(DTO):
    animal_id: int
    location_point_id: int


@dataclass
class ChangeAnimalVisitedLocationDTO(DTO):
    id: int
    animal_id: int
    location_point_id: int


@dataclass
class AnimalVisitedLocationDTO(DTO):
    id: int
    datetime_of_visit: datetime
    location_point_id: int


@dataclass
class AnimalVisitedLocationDTOs(DTO):
    visited_locations: List[AnimalVisitedLocationDTO]
