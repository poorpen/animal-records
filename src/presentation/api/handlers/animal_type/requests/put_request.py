from pydantic import BaseModel, Field


class ChangeAnimalTypeVM(BaseModel):
    animal_type: str = Field(alias='type')

    class Config:
        allow_population_by_field_name = True

