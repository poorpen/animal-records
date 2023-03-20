from src.domain.location_point.value_objects import LocationPointID, Latitude, Longitude
from src.domain.location_point.entities.location_point import LocationPoint

from src.application.location_point.dto.location_point import LocationPointDTO

from src.infrastructure.database.models.location_point import LocationPointDB

from src.infrastructure.mapper.decor import converter


def convert_to_dto(data: LocationPoint | LocationPointDB) -> LocationPointDTO:
    return LocationPointDTO(
        id=data.id,
        latitude=data.latitude,
        longitude=data.longitude

    )


@converter(LocationPoint, LocationPointDTO)
def location_point_entity_to_dto_converter(data: LocationPoint) -> LocationPointDTO:
    return LocationPointDTO(
        id=data.id.to_id(),
        latitude=data.latitude.to_fload(),
        longitude=data.longitude.to_fload()

    )


@converter(LocationPoint, LocationPointDB)
def location_point_entity_to_model_converter(data: LocationPoint) -> LocationPointDB:
    return LocationPointDB(
        id=data.id.to_id(),
        latitude=data.latitude.to_fload(),
        longitude=data.longitude.to_fload()
    )


@converter(LocationPointDB, LocationPoint)
def location_point_model_to_entity_converter(data: LocationPointDB) -> LocationPoint:
    return LocationPoint(
        id=LocationPointID(data.id),
        latitude=Latitude(data.latitude),
        longitude=Longitude(data.longitude)
    )


@converter(LocationPointDB, LocationPointDTO)
def location_point_model_to_dto_converter(data: LocationPointDB) -> LocationPointDTO:
    return convert_to_dto(data)
