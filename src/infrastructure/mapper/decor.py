from typing import Callable

from src.infrastructure.mapper.mapper import Mapper, FromModel, ToModel


def converter(from_model: FromModel, to_model: ToModel, func: Callable):
    def add_converter(mapper: Mapper):
        mapper.add(from_model=from_model, to_model=to_model, func=func)

    return add_converter
