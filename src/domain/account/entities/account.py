from __future__ import annotations

from dataclasses import dataclass

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter


@dataclass
class Account(Entity, EntityMerge):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str

    @staticmethod
    def create(first_name: str,
               last_name: str,
               email: str,
               password: str,
               account_id: int | None = None) -> Account:
        return Account(id=account_id, first_name=first_name, last_name=last_name, email=email, password=password)

    def update(self,
               first_name: str | Empty = Empty.UNSET,
               last_name: str | Empty = Empty.UNSET,
               email: str | Empty = Empty.UNSET,
               password: str | Empty = Empty.UNSET) -> None:
        filtered_args = data_filter(first_name=first_name, last_name=last_name, email=email)
        self._merge(**filtered_args)
