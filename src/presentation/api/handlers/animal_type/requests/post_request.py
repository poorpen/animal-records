from pydantic import BaseModel, Field


class CreateAnimalTypeVM(BaseModel):
    animal_type: str = Field(alias='type')
