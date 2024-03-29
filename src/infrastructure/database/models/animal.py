from sqlalchemy import Column, Integer, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.animal.enums import LifeStatus,Gender

from src.infrastructure.database.models.base import Base


class AnimalDB(Base):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    gender = Column(Enum(Gender))
    life_status = Column(Enum(LifeStatus))
    chipping_datetime = Column(DateTime(timezone=True))
    chipping_location_id = Column(ForeignKey('location_points.id'))
    chipper_id = Column(ForeignKey('accounts.id'))
    death_datetime = Column(DateTime(timezone=True), default=None)

    animal_types = relationship('TypeOfSpecificAnimalDB', lazy='joined', cascade="all, delete-orphan")
    visited_locations = relationship('AnimalVisitedLocationDB', lazy='joined', cascade="all, delete-orphan",
                                     order_by="asc(AnimalVisitedLocationDB.datetime_of_visit)")


