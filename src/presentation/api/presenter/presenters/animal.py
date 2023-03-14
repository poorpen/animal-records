from src.application.animal.dto.animal import AnimalDTO, AnimalDTOs
from src.application.animal.dto.animal_visited_location import AnimalVisitedLocationDTO, AnimalVisitedLocationDTOs

from src.infrastructure.mapper.decor import converter

from src.presentation.api.handlers.animal.responses.animal import AnimalVM, AnimalsVM
from src.presentation.api.handlers.animal.responses.animal_visited_location import AnimalVisitedLocationVM, \
    AnimaVisitedLocationsVM


def animal_dto_to_vm(data: AnimalDTO) -> AnimalVM:
    return AnimalVM(
        id=data.id,
        animal_types=data.animal_types,
        weight=data.weight,
        length=data.length,
        height=data.height,
        gender=data.gender,
        life_status=data.life_status,
        chipping_datetime=data.chipping_datetime.isoformat(),
        visited_locations=data.visited_locations,
        chipper_id=data.chipper_id,
        chipping_location_id=data.chipping_location_id,
        death_datetime=data.death_datetime.isoformat() if data.death_datetime else None

    )


def visited_location_dto_to_vm(data: AnimalVisitedLocationDTO) -> AnimalVisitedLocationVM:
    return AnimalVisitedLocationVM(
        id=data.id,
        datetime_of_visit=data.datetime_of_visit.isoformat(),
        location_point_id=data.location_point_id
    )


@converter(AnimalDTO, AnimalVM)
def convert_animal_dto_to_vm(data: AnimalDTO) -> AnimalVM:
    return animal_dto_to_vm(data)


@converter(AnimalDTOs, AnimalsVM)
def convert_animal_dtos_to_vms(data: AnimalDTOs) -> AnimalsVM:
    return AnimalsVM(animals=[animal_dto_to_vm(animal) for animal in data.animals])


@converter(AnimalVisitedLocationDTO, AnimalVisitedLocationVM)
def convert_visited_location_dto_to_vm(data: AnimalVisitedLocationDTO) -> AnimalVisitedLocationVM:
    return visited_location_dto_to_vm(data)


@converter(AnimalVisitedLocationDTOs, AnimaVisitedLocationsVM)
def convert_visited_location_dtos_to_vms(data: AnimalVisitedLocationDTOs) -> AnimaVisitedLocationsVM:
    AnimaVisitedLocationsVM(
        visited_locations=[visited_location_dto_to_vm(visited_location) for visited_location in data.visited_locations])
