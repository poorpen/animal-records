from __future__ import annotations
from datetime import datetime

from sqlalchemy import select, asc
from sqlalchemy.sql.selectable import Select

from src.infrastructure.database.repo.common.base_query_bilder import BaseQueryBuilder
from src.infrastructure.database.models.animal_visited_location import AnimalVisitedLocationDB


class GetVisitedLocationQuery(BaseQueryBuilder):

    def get_query(self,
                  start_datetime: datetime,
                  end_datetime: datetime,
                  offset: int,
                  limit: int,
                  ) -> Select:
        return (
            self._select(offset, limit)
            ._with_dates_filter(start_datetime, end_datetime)
            ._build()
        )

    def _select(self, offset: int, limit: int) -> GetVisitedLocationQuery:
        self._query = select(AnimalVisitedLocationDB).orber_by(asc(AnimalVisitedLocationDB.datetime_of_visit)).offset(
            offset).limit(limit)

        return self

    def _with_dates_filter(self, start_datetime, end_datetime) -> GetVisitedLocationQuery:
        if start_datetime and end_datetime:
            self._query = self._query.where(
                AnimalVisitedLocationDB.datetime_of_visit.between(start_datetime, end_datetime))
        elif start_datetime:
            self._query = self._query.where(AnimalVisitedLocationDB.datetime_of_visit >= start_datetime)
        elif end_datetime:
            self._query = self._query.where(AnimalVisitedLocationDB.datetime_of_visit <= end_datetime)

        return self
