from sqlalchemy import Column, Integer, String

from src.infrastructure.database.models.base import Base


class AnimalTypeDB(Base):
    __tablename__ = 'animal_types'

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True, nullable=False)
