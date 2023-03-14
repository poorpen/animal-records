from datetime import datetime
from pydantic import BaseModel

from src.domain.animal.value_objects.gender import Gender
from src.domain.animal.value_objects.life_status import LifeStatus


class SearchAnimalParameters(BaseModel):
    chipper_id: int
    chipping_location_id: int
    life_status: LifeStatus
    gender: Gender
    start_datetime: str
    end_datetime: str
    limit: int
    offset: int


class SearchAnimalVisitedLocationParameters(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    limit: int
    offset: int
