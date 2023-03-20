from pydantic import BaseModel, Field


class AnimalTypeVM(BaseModel):
    id: int = Field(alias='id')
    type: str = Field(alias='type')

    class Config:
        allow_population_by_field_name = True
