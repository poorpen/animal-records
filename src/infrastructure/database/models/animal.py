from datetime import datetime

from sqlalchemy import Column, Integer, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.animal.value_objects.gender import Gender
from src.domain.animal.value_objects.life_status import LifeStatus

from src.infrastructure.database.models.base import Base


class AnimalDB(Base):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    gender = Column(Enum(Gender))
    life_status = Column(Enum(LifeStatus))
    chipping_datetime = Column(DateTime(timezone=True), default=datetime.utcnow())
    chipping_location_id = Column(ForeignKey('location_points.id'))
    chipper_id = Column(ForeignKey('accounts.id'))
    death_datetime = Column(DateTime(timezone=True), default=None)

    animal_types = relationship('AnimalTypeDB', secondary='type_of_specific_animal', lazy='joined',
                                cascade="all, delete")
    visited_locations = relationship('AnimalVisitedLocationDB', lazy='joined', cascade="all, delete")
