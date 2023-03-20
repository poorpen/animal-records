from __future__ import annotations

from dataclasses import dataclass, fields

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter

from src.domain.location_point.value_objects import LocationPointID, Latitude, Longitude


@dataclass
class LocationPoint(Entity, EntityMerge):
    id: LocationPointID
    latitude: Latitude
    longitude: Longitude

    @staticmethod
    def create(latitude: Latitude,
               longitude: Longitude,
               ) -> LocationPoint:
        return LocationPoint(id=LocationPointID(None), latitude=latitude, longitude=longitude)

    def update(self,
               location_point: LocationPointID | Empty = Empty.UNSET,
               latitude: Latitude | Empty = Empty.UNSET,
               longitude: Longitude | Empty = Empty.UNSET) -> None:
        filtered_args = data_filter(id=location_point, longitude=longitude, latitude=latitude)
        self._merge(**filtered_args)
