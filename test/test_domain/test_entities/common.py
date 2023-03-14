import pytest

from datetime import datetime

from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.value_objects.gender import Gender

from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal
from src.domain.animal.entities.animal import Animal


@pytest.fixture
def animal():
    return Animal(id=1,
                  weight=1.1,
                  length=1.1,
                  height=1.1,
                  gender=Gender.OTHER,
                  life_status=LifeStatus.ALIVE,
                  chipping_location_id=1,
                  chipper_id=1,
                  animal_types=[],
                  visited_locations=[],
                  chipping_datetime=None,
                  death_datetime=None
                  )
