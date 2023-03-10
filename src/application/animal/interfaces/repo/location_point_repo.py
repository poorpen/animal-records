from typing import Protocol


class ILocationPointRepo(Protocol):

    async def check_exist(self, location_id: int) -> bool:
        raise NotImplementedError
