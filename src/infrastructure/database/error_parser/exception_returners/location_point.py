from src.domain.location_point.entities.location_point import LocationPoint

from src.application.location_point.exceptions.location_point import PointAlreadyExist


def point_already_exist(location_point: LocationPoint):
    return PointAlreadyExist(location_point.latitude, location_point.longitude)
