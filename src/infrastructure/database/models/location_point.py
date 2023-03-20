from sqlalchemy import Column, Integer, Float, UniqueConstraint, DECIMAL
from src.infrastructure.database.models.base import Base


class LocationPointDB(Base):
    __tablename__ = 'location_points'

    id = Column(Integer, primary_key=True)
    latitude = Column(DECIMAL, nullable=False)
    longitude = Column(DECIMAL, nullable=False)

    __table_args__ = (
        UniqueConstraint('latitude', 'longitude', name='location_coordinates'),
    )
