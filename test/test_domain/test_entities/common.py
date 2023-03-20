from datetime import datetime

import pytest

from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal
from src.domain.animal.enums import LifeStatus, Gender

from src.domain.animal.entities.animal import Animal
from src.domain.animal.values_objects.animal import Weight, Length, Height, GenderVO, LifeStatusVO, ChippingLocationID, \
    ChipperID
from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.values_objects.type_of_specific_animal import AnimalTypeID


@pytest.fixture
def animal():
    return Animal(
        id=AnimalID(1),
        animal_types=[],
        weight=Weight(1.1),
        length=Length(1.1),
        height=Height(1.1),
        gender=GenderVO('OTHER'),
        life_status=LifeStatusVO("ALIVE"),
        chipping_datetime=datetime.utcnow(),
        chipping_location_id=ChippingLocationID(1),
        chipper_id=ChipperID(1),
        death_datetime=None,
        visited_locations=[],

    )
