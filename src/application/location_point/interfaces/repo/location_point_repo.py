from typing import Protocol

from src.domain.location_point.value_objects import LocationPointID
from src.domain.location_point.entities.location_point import LocationPoint

from src.application.location_point.dto.location_point import LocationPointDTO


class ILocationPointRepo(Protocol):

    async def get_location_by_id(self, location_id: LocationPointID) -> LocationPoint:
        raise NotImplementedError

    async def add_location_point(self, location_point: LocationPoint) -> int:
        raise NotImplementedError

    async def change_location_point(self, location_point: LocationPoint) -> None:
        raise NotImplementedError

    async def delete_location_point(self, location_id: LocationPointID) -> None:
        raise NotImplementedError


class ILocationPointReader(Protocol):

    async def get_location_by_id(self, location_id: int) -> LocationPointDTO:
        raise NotImplementedError
