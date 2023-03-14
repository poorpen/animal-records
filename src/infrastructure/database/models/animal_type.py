from sqlalchemy import Column, Integer, String

from src.infrastructure.database.models.base import Base

from sqlalchemy.orm import declarative_base, validates


class AnimalTypeDB(Base):
    __tablename__ = 'animal_types'

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True, nullable=False)


