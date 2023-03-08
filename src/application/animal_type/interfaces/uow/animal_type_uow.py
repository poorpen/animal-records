from src.application.common.interfaces.uow.base import IUoW

from src.application.animal_type.interfaces.repo.animal_type_repo import IAnimalTypeReader, IAnimalTypeRepo


class IAnimalTypeUoW(IUoW):
    animal_type_repo: IAnimalTypeRepo
    animal_type_reader: IAnimalTypeReader


