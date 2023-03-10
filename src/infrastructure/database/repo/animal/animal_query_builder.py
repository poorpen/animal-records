from __future__ import annotations
from datetime import datetime

from sqlalchemy import select, asc
from sqlalchemy.sql.selectable import Select

from src.domain.animal.value_objects.gender import Gender
from src.domain.animal.value_objects.life_status import LifeStatus

from src.infrastructure.database.repo.common.base_query_bilder import BaseQueryBuilder
from src.infrastructure.database.models.animal import AnimalDB


class GetAnimalQuery(BaseQueryBuilder):

    def get_query(self,
                  start_datetime: datetime,
                  end_datetime: datetime,
                  chipper_id: int,
                  chipping_location_id: int,
                  life_status: LifeStatus,
                  gender: Gender,
                  offset: int,
                  limit: int
                  ) -> Select:
        return (
            self._select(offset, limit)
            ._with_dates_filter(start_datetime, end_datetime)
            ._with_chipper_id(chipper_id)
            ._with_chipping_location_id(chipping_location_id)
            ._with_life_status(life_status)
            ._with_gender(gender)
            ._build())

    def _select(self, offset: int, limit: int) -> GetAnimalQuery:
        self._query = select(AnimalDB).order_by(asc(AnimalDB.id)).offset(offset).limit(limit)

        return self

    def _with_dates_filter(self, start_datetime, end_datetime) -> GetAnimalQuery:
        if start_datetime and end_datetime:
            self._query = self._query.where(AnimalDB.chipping_datetime.between(start_datetime, end_datetime))
        elif start_datetime:
            self._query = self._query.where(AnimalDB.chipping_datetime >= start_datetime)
        elif end_datetime:
            self._query = self._query.where(AnimalDB.chipping_datetime <= end_datetime)
        return self

    def _with_chipper_id(self, chipper_id: int) -> GetAnimalQuery:
        if chipper_id:
            self._query = self._query.where(AnimalDB.chipper_id == chipper_id)

        return self

    def _with_chipping_location_id(self, chipping_location_id: int) -> GetAnimalQuery:
        if chipping_location_id:
            self._query = self._query.where(AnimalDB.chipping_location_id == chipping_location_id)

        return self

    def _with_life_status(self, life_status: LifeStatus) -> GetAnimalQuery:
        if life_status:
            self._query = self._query.where(AnimalDB.life_status == life_status)

        return self

    def _with_gender(self, gender: Gender) -> GetAnimalQuery:
        if gender:
            self._query = self._query.where(AnimalDB.gender == gender)

        return self
