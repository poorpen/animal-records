from typing import List
from pydantic import BaseModel, Field

from src.domain.animal.enums import LifeStatus, Gender


class AnimalVM(BaseModel):
    id: int = Field(alias='id')
    animal_types: List[int] = Field(alias='animalTypes')
    weight: float = Field(alias='weight')
    length: float = Field(alias='length')
    height: float = Field(alias='height')
    gender: Gender = Field(alias='gender')
    life_status: LifeStatus = Field(alias='lifeStatus')
    chipping_datetime: str = Field(alias='chippingDateTime')
    chipper_id: int = Field(alias='chipperId')
    chipping_location_id: int = Field(alias='chippingLocationId')
    visited_locations: List[int] = Field(alias='visitedLocations', default=[])
    death_datetime: str | None = Field(alias='deathDateTime')

    class Config:
        allow_population_by_field_name = True


class AnimalsVM(BaseModel):
    animals: List[AnimalVM]
