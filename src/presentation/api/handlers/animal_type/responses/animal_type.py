from pydantic import BaseModel, Field


class AnimalTypeVM(BaseModel):
    id: int = Field(alias='id')
    type: str = Field(alias='type')
