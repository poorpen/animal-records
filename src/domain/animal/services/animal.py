from datetime import datetime


from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.entities.animal import Animal


def set_death_datetime(animal: Animal) -> None:
    if animal.life_status == LifeStatus.DEAD:
        animal.death_datetime = datetime.utcnow()

