from unittest import mock

import pytest

from datetime import datetime

from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal
from src.domain.animal.exceptions.animal import AttemptToResurrectAnimal, ChippingLocationEqualFirstLocation
from src.domain.animal.value_objects.gender import Gender
from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.entities.animal import Animal
from src.domain.animal.services.animal import set_death_datetime, check_life_status_conflict, check_chipping_location

from src.domain.common.exceptions.validation import IntegerMin, EnumError

from test.test_domain.test_entities.common import animal


def test_add_animal_negative_first():
    args = [1.1, 1.2, 1.3, 2, 3]
    for arg in args:
        index_arg = args.index(arg)
        args[index_arg] = 0
        with pytest.raises(IntegerMin):
            Animal.create(
                animal_types=[1, 2, 3],
                weight=args[0],
                length=args[1],
                height=args[2],
                gender='MALE',
                chipping_location_id=args[3],
                chipper_id=args[4]
            )
        args[index_arg] = arg


def test_add_animal_negative_second():
    with pytest.raises(EnumError):
        Animal.create(
            animal_types=[1, 2, 3],
            weight=1.1,
            length=1.1,
            height=1.1,
            gender='HA-HA-HA',
            chipping_location_id=1,
            chipper_id=1
        )


def test_add_animal_negative_third():
    with pytest.raises(IntegerMin):
        Animal.create(
            animal_types=[1, 0, 3],
            weight=1.1,
            length=1.1,
            height=1.1,
            gender='HA-HA-HA',
            chipping_location_id=1,
            chipper_id=1
        )


@mock.patch('src.domain.animal.entities.animal.datetime')
def test_add_animal_positive(mock_datetime):
    returned_datetime = datetime.utcnow()
    mock_datetime.utcnow = mock.Mock(return_value=returned_datetime)
    animal = Animal.create(
        animal_types=[1, 2, 3],
        weight=1.1,
        length=1.1,
        height=1.1,
        gender='OTHER',
        chipping_location_id=1,
        chipper_id=1
    )
    expected = Animal(
        id=None,
        animal_types=[TypeOfSpecificAnimal(animal_id=None, animal_type_id=1),
                      TypeOfSpecificAnimal(animal_id=None, animal_type_id=2),
                      TypeOfSpecificAnimal(animal_id=None, animal_type_id=3)],
        height=1.1,
        gender=Gender.OTHER,
        life_status=LifeStatus.ALIVE,
        chipping_datetime=returned_datetime,
        chipping_location_id=1,
        chipper_id=1,
        death_datetime=None,
        visited_locations=[],
        length=1.1,
        weight=1.1

    )
    assert animal == expected


def test_update_animal_negative(animal):
    with pytest.raises(EnumError):
        animal.update(life_status='HE-HE-HA')


def test_update_positive(animal):
    animal.update(life_status="DEAD")
    assert animal.life_status == LifeStatus.DEAD


def test_set_death_datetime_negative(animal):
    set_death_datetime(animal)
    assert animal.life_status == LifeStatus.ALIVE
    assert animal.death_datetime is None


def test_set_death_datetime_positive(animal):
    animal.life_status = LifeStatus.DEAD
    set_death_datetime(animal)
    assert isinstance(animal.death_datetime, datetime)


def test_life_status_conflict(animal):
    with pytest.raises(AttemptToResurrectAnimal):
        animal.life_status = LifeStatus.DEAD
        check_life_status_conflict(animal, 'ALIVE')


def test_check_chipping_location(animal):
    location_point_id = 22
    animal.visited_locations.append(
        AnimalVisitedLocation(id=1, datetime_of_visit=datetime.utcnow(), location_point_id=22))
    with pytest.raises(ChippingLocationEqualFirstLocation):
        check_chipping_location(animal, location_point_id)
