from pydantic import BaseModel, Field, conlist

class CreateAnimalVM(BaseModel):
    animal_types: conlist(int, min_items=1) = Field(alias='animalTypes')
    weight: float = Field(alias='weight')
    length: float = Field(alias='length')
    height: float = Field(alias='height')
    gender: str = Field(alias='gender')
    chipper_id: int = Field(alias='chipperId')
    chipping_location_id: int = Field(alias='chippingLocationId')


    class Config:
        allow_population_by_field_name = True
