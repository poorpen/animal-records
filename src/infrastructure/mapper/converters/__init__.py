from . import account, location_point, animal_type, animal

from src.infrastructure.mapper.mapper import Mapper


def bind_account_converters(mapper: Mapper):
    account.account_entity_to_dto_converter(mapper=mapper)
    account.account_entity_to_model_converter(mapper=mapper)
    account.account_model_to_entity_converter(mapper=mapper)
    account.account_model_to_dto_converter(mapper=mapper)
    account.account_models_to_dtos_converter(mapper=mapper)
    account.account_dto_to_entity_converter(mapper=mapper)


def bind_location_point_converters(mapper: Mapper):
    location_point.location_point_entity_to_dto_converter(mapper=mapper)
    location_point.location_point_entity_to_model_converter(mapper=mapper)
    location_point.location_point_model_to_entity_converter(mapper=mapper)
    location_point.location_point_model_to_dto_converter(mapper=mapper)


def bind_animal_type_converters(mapper: Mapper):
    animal_type.animal_type_entity_to_dto_converter(mapper=mapper)
    animal_type.anima_type_entity_to_model_converter(mapper=mapper)
    animal_type.animal_type_model_to_entity_converter(mapper=mapper)
    animal_type.animal_type_model_to_dto_converter(mapper=mapper)


def bind_animal_converters(mapper: Mapper):
    animal.visited_location_entity_to_dto(mapper=mapper)
    animal.visited_location_models_to_dtos_converter(mapper=mapper)

    animal.animal_entity_to_dto_converter(mapper=mapper)
    animal.animal_entity_to_model_converter(mapper=mapper)
    animal.animal_model_to_entity_converter(mapper=mapper)
    animal.animal_model_to_dto_converter(mapper=mapper)
    animal.animal_model_to_dtos_converter(mapper=mapper)
