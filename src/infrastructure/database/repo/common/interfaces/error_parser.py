from typing import Protocol
from sqlalchemy.exc import DatabaseError

from src.domain.common.entities.entity import Entity

from src.application.common.exceptions.application import ApplicationException


class IErrorParser(Protocol):

    def parse_error(self, entity: Entity, error: DatabaseError) -> ApplicationException:
        raise NotImplementedError
