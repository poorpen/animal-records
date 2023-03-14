from pydantic import BaseModel, Field


class ChangeAnimalTypeVM(BaseModel):
    animal_type: str = Field(alias='type')

