from pydantic import BaseModel, Field


class ChangeLocationPointVM(BaseModel):
    latitude: float = Field(alias='latitude')
    longitude: float = Field(alias='longitude')
