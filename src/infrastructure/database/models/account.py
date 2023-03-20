from sqlalchemy import Column, Integer, String

from src.infrastructure.database.models.base import Base


class AccountDB(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
