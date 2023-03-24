from decimal import Decimal

from sqlalchemy import insert, select, delete

from sqlalchemy.exc import IntegrityError

from src.domain.location_point.entities.location_point import LocationPoint

from src.application.common.exceptions.application import ApplicationException
from src.application.location_point.exceptions.location_point import PointNotFound, AnimalAssociatedWithPoint, \
    PointAlreadyExist
from src.application.location_point.dto.location_point import LocationPointDTO
from src.application.location_point.interfaces.repo.location_point_repo import ILocationPointRepo, ILocationPointReader
from src.domain.location_point.value_objects import LocationPointID

from src.infrastructure.database.repo.common.base_repo import SQLAlchemyRepo
from src.infrastructure.database.models.location_point import LocationPointDB


class LocationPointRepo(SQLAlchemyRepo, ILocationPointRepo):

    async def add_location_point(self, location_point: LocationPoint) -> int:
        sql = insert(LocationPointDB).values(latitude=location_point.latitude.to_fload(),
                                             longitude=location_point.longitude.to_fload()).returning(
            LocationPointDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError as exc:
            raise self._error_parser(location_point, exc)
        row_id = result.scalar()
        return row_id

    async def get_location_by_id(self, location_id: LocationPointID) -> LocationPoint:
        sql = select(LocationPointDB).where(LocationPointDB.id == location_id.to_id())
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise PointNotFound(location_id.to_id())
        return self._mapper.load(LocationPoint, model)

    async def change_location_point(self, location_point: LocationPoint) -> None:
        location_point_db = self._mapper.load(LocationPointDB, location_point)
        try:
            await self._session.merge(location_point_db)
            await self._session.flush()
        except IntegrityError as exc:
            raise self._error_parser(location_point, exc)

    async def delete_location_point(self, location_id: LocationPointID) -> None:
        sql = delete(LocationPointDB).where(LocationPointDB.id == location_id.to_id()).returning(LocationPointDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError:
            raise AnimalAssociatedWithPoint(location_id.to_id())
        deleted_row_id = result.scalar()
        if not deleted_row_id:
            raise PointNotFound(location_id.to_id())

    @staticmethod
    def _error_parser(location_point: LocationPoint, exception: IntegrityError) -> ApplicationException:
        database_column = exception.__cause__.__cause__.constraint_name
        if database_column == 'location_coordinates':
            return PointAlreadyExist(latitude=location_point.latitude.to_fload(),
                                     longitude=location_point.longitude.to_fload())


class LocationPointReader(SQLAlchemyRepo, ILocationPointReader):

    async def get_location_by_id(self, location_id: int) -> LocationPointDTO:
        self._validate_id(location_id, 'location_id')
        sql = select(LocationPointDB).where(LocationPointDB.id == location_id)
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise PointNotFound(location_id)
        return self._mapper.load(LocationPointDTO, model)
