from pydantic import BaseModel, Field


class UpdateAnimalVM(BaseModel):
    life_status: str = Field(alias='lifeStatus')
    weight: float = Field(alias='weight')
    length: float = Field(alias='length')
    height: float = Field(alias='height')
    chipper_id: int = Field(alias='chipperId')
    chipping_location_id: int = Field(alias='chippingLocationId')
    gender: str = Field(alias='gender')

    class Config:
        allow_population_by_field_name = True


class ChangeTypeOfSpecificAnimalVM(BaseModel):
    old_type_id: int = Field(alias='oldTypeId')
    new_type_id: int = Field(alias='newTypeId')

    class Config:
        allow_population_by_field_name = True

class ChangeAnimalVisitedLocationVM(BaseModel):
    visited_location_point_id: int = Field(alias='visitedLocationPointId')
    location_point_id: int = Field(alias='locationPointId')

    class Config:
        allow_population_by_field_name = True
