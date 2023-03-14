from __future__ import annotations

from dataclasses import dataclass, fields

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter

from src.domain.common.validations.int_fields_validations import validation_of_max_allowable_int, \
    validation_of_min_allowable_int


@dataclass
class LocationPoint(Entity, EntityMerge):
    id: int
    latitude: float
    longitude: float

    @staticmethod
    def create(latitude: float,
               longitude: float,
               location_id: int | None = None
               ) -> LocationPoint:
        return LocationPoint(id=location_id, latitude=latitude, longitude=longitude)

    def update(self,
               latitude: float | Empty = Empty.UNSET,
               longitude: float | Empty = Empty.UNSET) -> None:
        filtered_args = data_filter(longitude=longitude, latitude=latitude)
        self._merge(**filtered_args)

    @staticmethod
    def _validate_data(name: str, value: str | int | float) -> None:
        min_value, max_value = None, None
        if isinstance(value, float) and name != 'latitude':
            min_value, max_value = -90, 90
        elif isinstance(value, float) and name != 'longitude':
            min_value, max_value = -180, 180

        if min_value and max_value:
            validation_of_min_allowable_int(field_name=name, min_integer=min_value, v=value, flag='<')
            validation_of_max_allowable_int(field_name=name, max_integer=max_value, v=value, flag='>')

    def __post_init__(self):
        for field in fields(self):
            name = field.name
            values = getattr(self, field.name)
            self._validate_data(name, values)

    def __post_merge__(self):
        for field in fields(self):
            name = field.name
            values = getattr(self, field.name)
            self._validate_data(name, values)
