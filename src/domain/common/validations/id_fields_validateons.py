from typing import List

from src.domain.common.entities.entity import Entity

from src.domain.common.exceptions.validation import IntegerMin


def check_valid_ids_animal_types(v: List[Entity], name: str):
    for entity in v:
        if entity.animal_type_id <= 0:
            raise IntegerMin(name, 0)


def check_valid_ids_visited_location(v: List[Entity], name: str):
    for entity in v:
        if entity.id <= 0:
            raise IntegerMin(name, 0)
