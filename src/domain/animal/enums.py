from enum import Enum


class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'


class LifeStatus(Enum):
    ALIVE = 'ALIVE'
    DEAD = 'DEAD'
