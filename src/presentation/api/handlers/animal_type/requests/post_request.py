from pydantic import BaseModel, Field


class AddAnimalTypeVM(BaseModel):
    animal_type: str = Field(alias='type')
