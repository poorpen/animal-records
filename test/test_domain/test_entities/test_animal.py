from unittest import mock

import pytest

from datetime import datetime

from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal
from src.domain.animal.exceptions.animal import AttemptToResurrectAnimal, ChippingLocationEqualFirstLocation
from src.domain.animal.enums import LifeStatus, Gender
from src.domain.animal.entities.animal import Animal
from src.domain.animal.services.animal import set_death_datetime, check_life_status_conflict, check_chipping_location

from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.values_objects.animal import LifeStatusVO, GenderVO, Height, Length, Weight, ChipperID, \
    ChippingLocationID
from src.domain.animal.values_objects.animal_visited_location import VisitedLocationID, LocationPointID
from src.domain.animal.values_objects.type_of_specific_animal import AnimalTypeID

from src.domain.common.exceptions.validation import IntegerMin, EnumError, InvalidID

from test.test_domain.test_entities.common import animal


def test_add_animal_negative_first():
    args = [1.1, 1.2, 1.3]
    for arg in args:
        index_arg = args.index(arg)
        args[index_arg] = 0
        with pytest.raises(IntegerMin):
            Animal.create(
                animal_types=[1, 2, 3],
                weight=Weight(args[0]),
                length=Length(args[1]),
                height=Height(args[2]),
                gender=GenderVO('MALE'),
                chipping_location_id=ChippingLocationID(1),
                chipper_id=ChipperID(1)
            )
        args[index_arg] = arg


def test_add_animal_negative_second():
    with pytest.raises(EnumError):
        Animal.create(
            animal_types=[1, 2, 3],
            weight=Weight(1.1),
            length=Length(1.1),
            height=Height(1.1),
            gender=GenderVO('HA-HA-HA'),
            chipping_location_id=ChippingLocationID(1),
            chipper_id=ChipperID(1)
        )


def test_add_animal_negative_third():
    ids = [1, 1]
    for id_ in ids:
        id_index = ids.index(id_)
        ids[id_index] = -1
        with pytest.raises(InvalidID):
            Animal.create(
                animal_types=[1, 0, 3],
                weight=Weight(1.1),
                length=Length(1.1),
                height=Height(1.1),
                gender=GenderVO('OTHER'),
                chipping_location_id=ChippingLocationID(ids[0]),
                chipper_id=ChipperID(ids[1])
            )
        ids[id_index] = id_


def test_add_animal_negative_fifth():
    with pytest.raises(InvalidID):
        Animal.create(
            animal_types=[1, 0, 3],
            weight=Weight(1.1),
            length=Length(1.1),
            height=Height(1.1),
            gender=GenderVO('OTHER'),
            chipping_location_id=ChippingLocationID(1),
            chipper_id=ChipperID(1)
        )


@mock.patch('src.domain.animal.entities.animal.datetime')
def test_add_animal_positive(mock_datetime, animal):
    animal.id = AnimalID(None)
    returned_datetime = datetime.utcnow()
    animal.chipping_datetime = returned_datetime
    mock_datetime.utcnow = mock.Mock(return_value=returned_datetime)
    new_animal = Animal.create(
        animal_types=[1, 2, 3],
        weight=Weight(1.1),
        length=Length(1.1),
        height=Height(1.1),
        gender=GenderVO('OTHER'),
        chipping_location_id=ChippingLocationID(1),
        chipper_id=ChipperID(1)
    )
    expected = animal
    expected.animal_types = [TypeOfSpecificAnimal(animal_id=AnimalID(None), animal_type_id=AnimalTypeID(1)),
                             TypeOfSpecificAnimal(animal_id=AnimalID(None), animal_type_id=AnimalTypeID(2)),
                             TypeOfSpecificAnimal(animal_id=AnimalID(None), animal_type_id=AnimalTypeID(3))]
    expected.visited_locations = [None]
    assert new_animal == expected


def test_update_animal_negative(animal):
    with pytest.raises(EnumError):
        animal.update(life_status=LifeStatusVO('HE-HE-HA'))


def test_update_positive(animal):
    animal.update(life_status=LifeStatusVO("DEAD"))
    assert animal.life_status.to_enum() == LifeStatus.DEAD


def test_set_death_datetime_negative(animal):
    set_death_datetime(animal)
    assert animal.life_status.to_enum() == LifeStatus.ALIVE
    assert animal.death_datetime is None


def test_set_death_datetime_positive(animal):
    animal.life_status.value = 'DEAD'
    set_death_datetime(animal)
    assert isinstance(animal.death_datetime, datetime)


def test_life_status_conflict(animal):
    animal.id = AnimalID(1)
    with pytest.raises(AttemptToResurrectAnimal):
        animal.life_status.value = "DEAD"
        check_life_status_conflict(animal, 'ALIVE')


def test_check_chipping_location(animal):
    animal.id = AnimalID(2)
    location_point_id = LocationPointID(22)
    animal.chipping_location_id.value = location_point_id
    animal.visited_locations.append(
        AnimalVisitedLocation(id=VisitedLocationID(1), datetime_of_visit=datetime.utcnow(),
                              location_point_id=LocationPointID(22), animal_id=AnimalID(2)))
    with pytest.raises(ChippingLocationEqualFirstLocation):
        check_chipping_location(animal, location_point_id.to_id())
