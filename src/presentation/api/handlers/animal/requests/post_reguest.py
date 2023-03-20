from typing import List

from pydantic import BaseModel, Field


class CreateAnimalVM(BaseModel):
    animal_types: List[int] = Field(alias='animalTypes')
    weight: float = Field(alias='weight')
    length: float = Field(alias='length')
    height: float = Field(alias='height')
    gender: str = Field(alias='gender')
    chipper_id: int = Field(alias='chipperId')
    chipping_location_id: int = Field(alias='chippingLocationId')
