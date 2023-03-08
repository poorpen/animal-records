from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class IMapper(Protocol):

    def load(self, class_: type[T], data: Any):
        raise NotImplementedError
