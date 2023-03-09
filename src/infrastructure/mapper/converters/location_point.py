from src.domain.location_point.entities.location_point import LocationPoint

from src.application.location_point.dto.location_point import LocationPointDTO

from src.infrastructure.database.models.location_point import LocationPointDB


def location_point_entity_to_dto(data: LocationPoint) -> LocationPointDTO:
    return LocationPointDTO(
        id=data.id,
        latitude=data.latitude,
        longitude=data.longitude

    )


def location_point_entity_to_model(data: LocationPoint) -> LocationPointDB:
    return LocationPointDB(
        id=data.id,
        latitude=data.latitude,
        longitude=data.longitude
    )


def location_point_model_to_entity(data: LocationPointDB) -> LocationPoint:
    return LocationPoint(
        id=data.id,
        latitude=data.latitude,
        longitude=data.longitude
    )


def location_point_model_to_dto(data: LocationPointDB) -> LocationPointDTO:
    return LocationPointDTO(
        id=data.id,
        latitude=data.latitude,
        longitude=data.longitude
    )
