from datetime import datetime

from typing import Protocol

from src.domain.animal.values_objects.common import AnimalID
from src.application.animal.dto.animal_visited_location import AnimalVisitedLocationDTOs


class IAnimalVisitedLocationReader(Protocol):

    async def get_visited_locations(self,
                                    animal_id: int,
                                    start_datetime: datetime,
                                    end_datetime: datetime,
                                    limit: int,
                                    offset: int
                                    ) -> AnimalVisitedLocationDTOs:
        raise NotImplementedError
