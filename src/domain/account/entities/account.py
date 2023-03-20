from __future__ import annotations

from dataclasses import dataclass, fields

from src.domain.common.entities.entity import Entity
from src.domain.common.entities.entity_merge import EntityMerge

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter

from src.domain.account.value_objects import AccountID, FirstName, LastName, Email


@dataclass
class Account(Entity, EntityMerge):
    id: AccountID
    first_name: FirstName
    last_name: LastName
    email: Email
    password: str

    @staticmethod
    def create(first_name: FirstName,
               last_name: LastName,
               email: Email,
               password: str) -> Account:
        return Account(id=AccountID(None), first_name=first_name, last_name=last_name, email=email, password=password)

    def update(self,
               account_id: AccountID | Empty = Empty.UNSET,
               first_name: FirstName | Empty = Empty.UNSET,
               last_name: LastName | Empty = Empty.UNSET,
               email: Email | Empty = Empty.UNSET,
               password: str | Empty = Empty.UNSET) -> None:
        filtered_args = data_filter(first_name=first_name, last_name=last_name, email=email, password=password,
                                    id=account_id)
        self._merge(**filtered_args)
