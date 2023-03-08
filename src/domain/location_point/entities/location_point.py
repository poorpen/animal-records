from __future__ import annotations

from dataclasses import dataclass

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter


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
