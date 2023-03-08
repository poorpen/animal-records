from sqlalchemy import Column, Integer, Float
from src.infrastructure.database.models.base import Base


class LocationPointDB(Base):
    __tablename__ = 'location_points'

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, unique=True, nullable=False)
    longitude = Column(Float, unique=True, nullable=False)

