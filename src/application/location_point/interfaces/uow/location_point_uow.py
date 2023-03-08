from src.application.common.interfaces.uow.base import IUoW

from src.application.location_point.interfaces.repo.location_point_repo import ILocationPointReader, ILocationPointRepo


class ILocationPointUoW(IUoW):
    location_point_repo: ILocationPointRepo
    location_point_reader: ILocationPointReader
