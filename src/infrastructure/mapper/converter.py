from typing import Callable, TypeVar, Any

FromModel = TypeVar("FromModel", bound=Any)
ToModel = TypeVar("ToModel", bound=Any)


class Converter:

    def __init__(self, from_model: FromModel, to_mode: ToModel, func: Callable):
        self._from_model = from_model
        self._to_model = to_mode
        self.func = func

    def  check(self, from_model: FromModel, to_model: ToModel):
        if self._from_model == from_model and self._to_model == to_model:
            return True
        return False

    def convert(self, data: Any):
        self.func(data)
