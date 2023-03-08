from src.application.common.interfaces.uow.base import IUoW

from src.application.animal.interfaces.repo.animal_type_repo import IAnimalTypeRepo


class IAnimalTypeUoW(IUoW):
    animal_type_repo: IAnimalTypeRepo
