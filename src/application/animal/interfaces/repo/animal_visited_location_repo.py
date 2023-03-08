from datetime import datetime

from typing import Protocol, List

from src.application.animal.dto.animal_visited_location import AnimalVisitedLocationDTO


class IAnimalVisitedLocationRepo(Protocol):

    async def check_exist_visited_location(self, visited_location_id: int) -> bool:
        raise NotImplementedError


class IAnimalVisitedLocationReader(Protocol):

    async def get_visited_locations(self,
                                    animal_id: int,
                                    start_datetime: datetime,
                                    end_datetime: datetime,
                                    limit: int,
                                    offset: int
                                    ) -> List[AnimalVisitedLocationDTO]:
        raise NotImplementedError
