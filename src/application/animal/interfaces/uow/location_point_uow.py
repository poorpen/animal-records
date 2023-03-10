from src.application.common.interfaces.uow.base import IUoW

from src.application.animal.interfaces.repo.location_point_repo import ILocationPointRepo


class ILocationPointUoW(IUoW):
    location_point_repo: ILocationPointRepo
