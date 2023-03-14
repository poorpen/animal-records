from typing import List
from pydantic import BaseModel, Field

from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.value_objects.gender import Gender


class AnimalVM(BaseModel):
    id: int = Field(alias='id')
    animal_types: List[int] = Field('animalTypes')
    weight: float = Field(alias='weight')
    length: float = Field(alias='length')
    height: float = Field(alias='height')
    gender: Gender = Field(alias='gender')
    life_status: LifeStatus = Field(alias='lifeStatus')
    chipping_datetime: str = Field(alias='chippingDateTime')
    chipper_id: int
    chipping_location_id: int = Field(alias='chippingLocationId')
    visited_locations: List[int] = Field(alias='visitedLocations')
    death_datetime: str | None = Field(alias='deathDateTime')


class AnimalsVM(BaseModel):
    animals: List[AnimalVM]
