from pydantic import BaseModel, Field


class UpdateAnimalVM(BaseModel):
    weight: float = Field(alias='weight')
    length: float = Field(alias='length')
    height: float = Field(alias='height')
    gender: str = Field(alias='gender')
    life_status: str = Field(alias='lifeStatus')
    chipper_id: int = Field(alias='chipperId')
    chipping_location_id: int = Field(alias='chippingLocationId')


class ChangeTypeOfSpecificAnimalVM(BaseModel):
    old_type_id: int = Field(alias='oldTypeId')
    new_type_id: int = Field(alias='newTypeId')
