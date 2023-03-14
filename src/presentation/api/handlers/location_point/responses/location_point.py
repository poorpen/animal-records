from pydantic import BaseModel, Field


class LocationPointVM(BaseModel):
    id: int = Field(alias='id')
    latitude: float = Field(alias='latitude')
    longitude: float = Field(alias='longitude')
