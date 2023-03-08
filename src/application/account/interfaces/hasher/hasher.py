from typing import Protocol


class IHasher(Protocol):

    def hash(self, row: str) -> str:
        raise NotImplementedError

    def verify(self, row: str, hashed_row: str) -> bool:
        raise NotImplementedError
