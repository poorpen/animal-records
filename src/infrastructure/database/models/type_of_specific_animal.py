from sqlalchemy import Column,  ForeignKey

from src.infrastructure.database.models.base import Base


class TypeOfSpecificAnimalDB(Base):
    __tablename__ = 'type_of_specific_animal'

    animal_id = Column(ForeignKey('animals.id', ondelete="CASCADE"), primary_key=True)
    animal_type_id = Column(ForeignKey('animal_types.id'), primary_key=True)
