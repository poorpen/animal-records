from . import account, animal, animal_type, location_point

from src.presentation.api.presenter.presenter import Presenter


def bind_account_presenter(presenter: Presenter):
    account.convert_dto_to_vm(mapper=presenter)
    account.convert_dtos_to_vms(mapper=presenter)


def bind_animal_presenter(presenter: Presenter):
    animal.convert_visited_location_dto_to_vm(mapper=presenter)
    animal.convert_visited_location_dtos_to_vms(mapper=presenter)

    animal.convert_animal_dto_to_vm(mapper=presenter)
    animal.convert_animal_dtos_to_vms(mapper=presenter)


def bind_animal_type_presenter(presenter: Presenter):
    animal_type.convert_animal_type_dto_to_vm(mapper=presenter)


def bind_location_point_presenter(presenter: Presenter):
    location_point.convert_dto_to_vm(mapper=presenter)
