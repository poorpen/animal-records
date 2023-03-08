from sqlalchemy.sql.selectable import Select


class BaseQueryBuilder:

    def __init__(self):
        self._query = None

    def _build(self):
        return self._query

    def get_query(self, *args, **kwargs) -> Select:
        ...
