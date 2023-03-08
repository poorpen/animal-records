from src.application.common.interfaces.uow.base import IUoW

from src.application.animal.interfaces.repo.animal_repo import IAnimalRepo, IAnimalReader


class IAnimalUoW(IUoW):
    animal_repo: IAnimalRepo
    animal_reader: IAnimalReader
