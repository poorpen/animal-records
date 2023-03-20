from src.domain.common.value_objects.id import IDVO
from src.domain.common.value_objects.text import TextVO


class AnimalTypeID(IDVO):
    __field_name__ = 'type_id'


class AnimalTypeName(TextVO):
    __field_name__ = 'type'
