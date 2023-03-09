from typing import TypeVar, Any, Callable, List

from src.application.common.interfaces.mapper import IMapper

from src.infrastructure.mapper.converter import Converter, ToModel, FromModel

T = TypeVar("T")


class Mapper(IMapper):

    def __init__(self):
        self._converters: List[Converter] = []

    def add(self, from_model: FromModel, to_model: ToModel, func: Callable) -> None:
        self._converters.append(
            Converter(from_model=from_model,
                      to_mode=to_model,
                      func=func)
        )

    def load(self, class_: type[T], data: Any) -> T:
        converter = self._get_converter(from_mode=type(data), to_model=class_)
        converter.convert(data)

    def _get_converter(self, from_mode: FromModel, to_model: ToModel) -> Converter:
        for converter in self._converters:
            if converter.check(from_mode, to_model):
                return converter
