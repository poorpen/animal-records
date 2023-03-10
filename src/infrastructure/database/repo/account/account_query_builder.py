from __future__ import annotations

from sqlalchemy import select, func, asc
from sqlalchemy.sql.selectable import Select

from src.infrastructure.database.models.account import AccountDB
from src.infrastructure.database.repo.common.base_query_bilder import BaseQueryBuilder


class GetAccountQuery(BaseQueryBuilder):

    def get_query(self,
                  first_name: str,
                  last_name: str,
                  email: str,
                  offset: int,
                  limit: int,
                  ) -> Select:
        return (
            self._select(offset, limit)
            ._with_first_name(first_name)
            ._with_last_name(last_name)
            ._with_email(email)
            ._build()
        )

    def _select(self, offset: int, limit: int) -> GetAccountQuery:
        self._query = select(AccountDB).order_by(asc(AccountDB.id)).offset(offset).limit(limit)
        return self

    def _with_first_name(self, first_name: str) -> GetAccountQuery:
        if first_name:
            self._query = self._query.where(AccountDB.first_name == first_name)

        return self

    def _with_last_name(self, last_name: str) -> GetAccountQuery:
        if last_name:
            self._query = self._query.where(AccountDB.last_name == last_name)

        return self

    def _with_email(self, email: str) -> GetAccountQuery:
        if email:
            self._query = self._query.where(func.lower(AccountDB.email).like(func.lower(f'%{email}%')))

        return self

    def _build(self):
        return self._query
