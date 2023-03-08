from src.domain.animal_type.entities.animal_type import AnimalType

from src.application.animal_type.exceptions.animal_type import AnimalTypeAlreadyExist


def animal_type_already_exist(animal_type: AnimalType):
    return AnimalTypeAlreadyExist(animal_type.type)
