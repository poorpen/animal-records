from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field, validator

from src.domain.common.exceptions.validation import BaseModelException


@dataclass
class ISODateTimeError(BaseModelException):
    time_str: str

    def message(self):
        return f'переданная вами строка {self.time_str} не соответствует ISO формату'


class SearchAnimalParametersVM(BaseModel):
    start_datetime: str = Field(alias='startDateTime', default='')
    end_datetime: str = Field(alias='endDateTime', default='')
    chipper_id: int | str = Field(alias='chipperId', default='')
    chipping_location_id: int | str = Field(alias='chippingLocationId', default='')
    life_status: str = Field(alias='lifeStatus', default='')
    gender: str = Field(alias='gender', default='')
    offset: int = Field(default=0)
    limit: int = Field(alias='size', default=10)

    @validator('start_datetime', 'end_datetime')
    def validate_datetime(cls, v, field):
        if v:
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ISODateTimeError(field.name, v)

    class Config:
        allow_population_by_field_name = True


class SearchAnimalVisitedLocationParametersVM(BaseModel):
    start_datetime: str = Field(alias='startDateTime', default='')
    end_datetime: str = Field(alias='endDateTime', default='')
    offset: int = Field(default=0)
    limit: int = Field(alias='size', default=10)

    @validator('start_datetime', 'end_datetime')
    def validate_datetime(cls, v, field):
        if v:
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ISODateTimeError(field.name, v)

    class Config:
        allow_population_by_field_name = True
