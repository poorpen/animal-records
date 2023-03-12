import pytest

from datetime import datetime

from src.domain.animal.value_objects.life_status import LifeStatus

from test.test_domain.test_entities.common import animal


def test_set_death_datetime_negative(animal):
    animal.set_death_datetime()
    assert animal.life_status == LifeStatus.ALIVE
    assert animal.death_datetime is None


def test_set_death_datetime_positive(animal):
    animal.life_status = LifeStatus.DEAD
    animal.set_death_datetime()
    assert isinstance(animal.death_datetime, datetime)