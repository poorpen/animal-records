import pytest

from src.domain.animal.services.type_of_specific_animal import add_animal_type, change_animal_type, delete_animal_type

from src.domain.animal.exceptions.type_of_specific_animal import AnimalNotHaveThisType, AnimalAlreadyHaveThisTypes, \
    AnimalAlreadyHaveThisType, AnimalOnlyHasThisType

from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal

from test.test_domain.test_entities.common import animal


@pytest.fixture
def old_type_id():
    return 4


@pytest.fixture
def new_type_id():
    return 6


def test_add_type_negative(animal):
    animal_type_id = 1
    add_animal_type(animal, animal_type_id)
    with pytest.raises(AnimalAlreadyHaveThisType):
        add_animal_type(animal, animal_type_id)


def test_add_type_positive(animal):
    animal_type_id = 2
    add_animal_type(animal, animal_type_id)
    expected_animal_type = TypeOfSpecificAnimal(None, animal_type_id)
    assert animal.get_animal_type(animal_type_id) == expected_animal_type


def test_check_duplicate_types_negative(animal):
    animal.animal_types.append(TypeOfSpecificAnimal(animal_id=animal.id, animal_type_id=3))
    duplicate = animal.check_duplicate_types()
    assert duplicate is None


def test_check_duplicate_types_positive(animal):
    animal_type_id = 2
    animal.animal_types.extend(
        [TypeOfSpecificAnimal(animal_id=animal.id, animal_type_id=animal_type_id),
         TypeOfSpecificAnimal(animal_id=animal.id, animal_type_id=animal_type_id)])
    expected_animal_type = TypeOfSpecificAnimal(animal_id=1, animal_type_id=animal_type_id)
    duplicate_type = animal.check_duplicate_types()
    assert duplicate_type == expected_animal_type


def test_change_animal_type_negative_first(animal, old_type_id, new_type_id):
    animal.update(animal_types=[TypeOfSpecificAnimal(animal_id=animal.id, animal_type_id=new_type_id),
                                TypeOfSpecificAnimal(animal_id=animal.id, animal_type_id=old_type_id)])
    with pytest.raises(AnimalAlreadyHaveThisTypes):
        change_animal_type(animal, old_type_id, new_type_id)


def test_change_animal_type_negative_second(animal, old_type_id, new_type_id):
    animal.update(animal_types=[TypeOfSpecificAnimal(animal_id=animal.id, animal_type_id=new_type_id)])
    with pytest.raises(AnimalAlreadyHaveThisType):
        change_animal_type(animal, old_type_id, new_type_id)


def test_change_animal_type_negative_third(animal, old_type_id, new_type_id):
    with pytest.raises(AnimalNotHaveThisType):
        change_animal_type(animal, old_type_id, new_type_id)


def test_change_type_positive(animal, old_type_id, new_type_id):
    animal_type = TypeOfSpecificAnimal(animal_id=animal.id, animal_type_id=old_type_id)
    animal.update(animal_types=[animal_type])
    old_type_index = animal.animal_types.index(animal_type)
    change_animal_type(animal, old_type_id, new_type_id)
    expected_type = TypeOfSpecificAnimal(animal_id=animal.id, animal_type_id=new_type_id)
    assert animal.animal_types[old_type_index] == expected_type


def test_delete_type_negative_first(animal):
    animal_typeid = 5
    animal.update(animal_types=[TypeOfSpecificAnimal(animal_id=animal.id, animal_type_id=animal_typeid)])
    with pytest.raises(AnimalOnlyHasThisType):
        delete_animal_type(animal, animal_typeid)


def test_delete_type_negative_second(animal):
    with pytest.raises(AnimalNotHaveThisType):
        delete_animal_type(animal, 1)


def test_delete_animal_positive(animal):
    animal_type_id = 5
    first_animal_type = TypeOfSpecificAnimal(animal_id=1, animal_type_id=animal_type_id)
    second_animal_type = TypeOfSpecificAnimal(animal_id=1, animal_type_id=7)
    animal.update(animal_types=[first_animal_type, second_animal_type])
    delete_animal_type(animal, animal_type_id)
    assert len(animal.animal_types) == 1 and first_animal_type not in animal.animal_types
