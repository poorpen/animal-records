from src.domain.common.exceptions.validation import IntegerMin, IntegerMax
from src.domain.common.value_objects.id import IDVO
from src.domain.common.value_objects.integer import FloatVO


class LocationPointID(IDVO):
    __field_name__ = 'point_id'


class LocationPointValidate(FloatVO):

    def __post_init__(self):
        if self.value < self.min_value:
            raise IntegerMin(field=self.__field_name__, min_integer=self.min_value)
        elif self.max_value and self.value > self.max_value:
            raise IntegerMax(field=self.__field_name__, max_integer=self.max_value)


class Latitude(LocationPointValidate):
    __field_name__ = 'latitude'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, min_value=-90, max_value=90)


class Longitude(LocationPointValidate):
    __field_name__ = 'longitude'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, min_value=-180, max_value=180)
