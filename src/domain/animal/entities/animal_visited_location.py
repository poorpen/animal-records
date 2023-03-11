from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter


@dataclass
class AnimalVisitedLocation(Entity, EntityMerge):
    id: int
    datetime_of_visit: datetime
    location_point_id: int

    @staticmethod
    def create(location_point_id: int,
               visited_location_id: int | None = None,
               datetime_of_visit: datetime | None = None
               ) -> AnimalVisitedLocation:
        return AnimalVisitedLocation(id=visited_location_id,
                                     datetime_of_visit=datetime_of_visit,
                                     location_point_id=location_point_id)

    def update(self, location_point_id: int | Empty = Empty.UNSET) -> None:
        filtered_args = data_filter(location_point_id=location_point_id)
        self._merge(**filtered_args)
