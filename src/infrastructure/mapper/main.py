from src.infrastructure.mapper.converters import bind_account_converters, bind_location_point_converters, \
    bind_animal_type_converters, bind_animal_converters

from src.infrastructure.mapper.mapper import Mapper


def build_mapper() -> Mapper:
    mapper = Mapper()
    bind_account_converters(mapper)
    bind_location_point_converters(mapper)
    bind_animal_type_converters(mapper)
    bind_animal_converters(mapper)
    return mapper
