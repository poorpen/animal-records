from typing import List
from pydantic import BaseModel, Field


class AnimalVisitedLocationVM(BaseModel):
    id: int = Field(alias='id')
    datetime_of_visit: str = Field(alias='dateTimeOfVisitLocationPoint')
    location_point_id: int = Field(alias='locationPointId')

    class Config:
        allow_population_by_field_name = True


class AnimaVisitedLocationsVM(BaseModel):
    visited_locations: List[AnimalVisitedLocationVM] = Field(default=[])
