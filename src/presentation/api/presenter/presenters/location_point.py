from src.application.location_point.dto.location_point import LocationPointDTO

from src.infrastructure.mapper.decor import converter

from src.presentation.api.handlers.location_point.responses.location_point import LocationPointVM


@converter(LocationPointDTO, LocationPointVM)
def convert_dto_to_vm(data: LocationPointDTO) -> LocationPointVM:
    return LocationPointVM(
        id=data.id,
        latitude=data.latitude,
        longitude=data.longitude
    )
