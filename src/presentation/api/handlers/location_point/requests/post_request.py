from pydantic import BaseModel, Field


class CreateLocationPointVM(BaseModel):
    latitude: float = Field(alias='latitude')
    longitude: float = Field(alias='longitude')
