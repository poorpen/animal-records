from .presenters import bind_account_presenter, bind_animal_presenter, bind_animal_type_presenter, \
    bind_location_point_presenter

from src.presentation.api.presenter.presenter import Presenter


def build_presenter():
    presenter = Presenter()
    bind_account_presenter(presenter)
    bind_animal_presenter(presenter)
    bind_animal_type_presenter(presenter)
    bind_location_point_presenter(presenter)
    return presenter
