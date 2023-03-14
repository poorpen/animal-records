from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal
from src.domain.animal.entities.animal import Animal

from src.domain.animal.exceptions.type_of_specific_animal import \
    AnimalAlreadyHaveThisType, AnimalAlreadyHaveThisTypes, AnimalOnlyHasThisType, AnimalNotHaveThisType

from src.domain.common.validations.int_fields_validations import validation_of_min_allowable_int


def add_animal_type(animal: Animal, type_id: int) -> None:
    type_of_this_animal = TypeOfSpecificAnimal.create(animal_type_id=type_id)
    if type_of_this_animal in animal.animal_types:
        raise AnimalAlreadyHaveThisType(animal.id, type_of_this_animal.animal_type_id)
    animal.update(animal_types=[type_of_this_animal])


def change_animal_type(animal: Animal, old_type_int: int, new_type_id: int) -> None:
    exist_old_type = animal.check_exist_animal_type(old_type_int)
    exist_new_type = animal.check_exist_animal_type(new_type_id)

    if exist_old_type and exist_new_type:
        raise AnimalAlreadyHaveThisTypes(animal_id=animal.id, old_type=old_type_int, new_type=new_type_id)
    elif exist_new_type:
        raise AnimalAlreadyHaveThisType(animal_id=animal.id, type_id=new_type_id)

    animal_type = animal.get_animal_type(old_type_int)
    index_animal_type = animal.animal_types.index(animal_type)
    animal.animal_types[index_animal_type].update(new_type_id)


def delete_animal_type(animal, animal_type_id: int) -> None:
    validation_of_min_allowable_int(animal_type_id, 'aninal_type_id', 0, '<=')
    type_of_this_animal = animal.get_animal_type(animal_type_id)
    if len(animal.animal_types) == 1 and animal.animal_types[0] == type_of_this_animal:
        raise AnimalOnlyHasThisType(animal.id, type_of_this_animal.animal_type_id)
    elif type_of_this_animal not in animal.animal_types:
        raise AnimalNotHaveThisType(animal.id, type_of_this_animal.animal_type_id)
    animal.animal_types.remove(type_of_this_animal)
