from sqlalchemy import Column, Integer, Float, UniqueConstraint
from src.infrastructure.database.models.base import Base


class LocationPointDB(Base):
    __tablename__ = 'location_points'

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('latitude', 'longitude', name='location_coordinates'),
    )
