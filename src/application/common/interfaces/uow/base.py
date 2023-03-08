from typing import Protocol


class IUoW(Protocol):

    async def commit(self):
        ...

    async def rollback(self):
        ...
