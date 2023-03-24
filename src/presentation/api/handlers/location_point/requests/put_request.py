from pydantic import BaseModel, Field


class ChangeLocationPointVM(BaseModel):
    latitude: float = Field(alias='latitude')
    longitude: float = Field(alias='longitude')

    class Config:
        allow_population_by_field_name = True
