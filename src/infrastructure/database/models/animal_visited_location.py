from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime

from src.infrastructure.database.models.base import Base


class AnimalVisitedLocationDB(Base):
    __tablename__ = 'animal_visited_location'

    id = Column(Integer, primary_key=True)
    animal_id = Column(ForeignKey('animals.id'))
    location_point_id = Column(ForeignKey('location_points.id'))
    datetime_of_visit = Column(DateTime(timezone=True))
