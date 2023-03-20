from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter

from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.values_objects.animal_visited_location import LocationPointID, VisitedLocationID


@dataclass
class AnimalVisitedLocation(Entity, EntityMerge):
    id: VisitedLocationID
    datetime_of_visit: datetime
    location_point_id: LocationPointID
    animal_id: AnimalID

    @staticmethod
    def create(location_point_id: LocationPointID,
               datetime_of_visit: datetime,
               animal_id: AnimalID = None) -> AnimalVisitedLocation:
        return AnimalVisitedLocation(id=VisitedLocationID(None),
                                     animal_id=animal_id,
                                     datetime_of_visit=datetime_of_visit,
                                     location_point_id=location_point_id)

    def update(self,
               visited_location_id: VisitedLocationID | Empty = Empty.UNSET,
               location_point_id: LocationPointID | Empty = Empty.UNSET) -> None:
        filtered_args = data_filter(location_point_id=location_point_id, id=visited_location_id)
        self._merge(**filtered_args)
