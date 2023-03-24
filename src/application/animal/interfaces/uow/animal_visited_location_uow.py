from src.application.common.interfaces.uow.base import IUoW

from src.application.animal.interfaces.repo.animal_visited_location_repo import IAnimalVisitedLocationReader


class IAnimalVisitedLocationUoW(IUoW):
    animal_reader: IAnimalVisitedLocationReader
