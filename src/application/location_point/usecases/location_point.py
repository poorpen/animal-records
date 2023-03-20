import logging.config

from abc import ABC

from src.domain.location_point.value_objects import LocationPointID, Latitude, Longitude

from src.domain.location_point.entities.location_point import LocationPoint

from src.application.common.interfaces.mapper import IMapper

from src.application.location_point.interfaces.uow.location_point_uow import ILocationPointUoW
from src.application.location_point.dto.location_point import LocationPointDTO, CreateLocationPointDTO, \
    ChangeLocationPointDTO
from src.application.location_point.exceptions.location_point import PointAlreadyExist, AnimalAssociatedWithPoint

logger = logging.getLogger(__name__)


class LocationPointUseCase(ABC):

    def __init__(self, uow: ILocationPointUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper


class CreateLocationPoint(LocationPointUseCase):

    async def __call__(self, location_point: CreateLocationPointDTO) -> LocationPointDTO:
        location_point = LocationPoint.create(
            longitude=Longitude(location_point.longitude),
            latitude=Latitude(location_point.latitude)
        )
        try:
            location_point_id = await self._uow.location_point_repo.add_location_point(location_point)
            await self._uow.commit()
        except PointAlreadyExist:
            await self._uow.rollback()
            raise
        location_point.update(LocationPointID(location_point_id))
        return self._mapper.load(LocationPointDTO, location_point)


class ChangeLocationPointUseCase(LocationPointUseCase):

    async def __call__(self, location_point_dto: ChangeLocationPointDTO) -> LocationPointDTO:
        location_point = await self._uow.location_point_repo.get_location_by_id(
            LocationPointID(location_point_dto.id))
        location_point.update(
            latitude=Latitude(location_point_dto.latitude),
            longitude=Longitude(location_point_dto.longitude)
        )
        try:
            await self._uow.location_point_repo.change_location_point(location_point)
            await self._uow.commit()
        except PointAlreadyExist:
            await self._uow.rollback()
            raise
        return self._mapper.load(LocationPointDTO, location_point)


class GetLocationPoint(LocationPointUseCase):

    async def __call__(self, location_point_id: int) -> LocationPointDTO:
        return await self._uow.location_point_reader.get_location_by_id(location_point_id)


class DeleteLocationPoint(LocationPointUseCase):

    async def __call__(self, location_point_id: int) -> None:
        try:
            await self._uow.location_point_repo.delete_location_point(LocationPointID(location_point_id))
            await self._uow.commit()
        except AnimalAssociatedWithPoint:
            await self._uow.rollback()
            raise


class LocationPointService:

    def __init__(self, uow: ILocationPointUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper

    async def create_location_point(self, location_point_dto: CreateLocationPointDTO) -> LocationPointDTO:
        return await CreateLocationPoint(self._uow, self._mapper)(location_point_dto)

    async def change_location_point(self, location_point_dto: ChangeLocationPointDTO) -> LocationPointDTO:
        return await ChangeLocationPointUseCase(self._uow, self._mapper)(location_point_dto)

    async def get_location_point(self, location_point_id: int) -> LocationPointDTO:
        return await GetLocationPoint(self._uow, self._mapper)(location_point_id)

    async def delete_location_point(self, location_point_id: int) -> None:
        await DeleteLocationPoint(self._uow, self._mapper)(location_point_id)
