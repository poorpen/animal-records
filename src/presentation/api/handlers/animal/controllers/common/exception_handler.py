from fastapi.responses import JSONResponse

from src.domain.animal.exceptions.common import DomainException
from src.domain.animal.exceptions import animal as animal_domain
from src.domain.animal.exceptions import animal_visited_location as animal_visited_location_domain
from src.domain.animal.exceptions import type_of_specific_animal as type_of_specific_animal_domain

from src.application.animal.exceptions.animal import BaseAnimalException

from src.application.animal.exceptions import animal, animal_visited_location
from src.application.animal_type.exceptions import animal_type
from src.application.location_point.exceptions import location_point
from src.application.account.exceptions import account


def animal_exception_handler(_, err: BaseAnimalException | DomainException):
    match err:
        case (animal_visited_location_domain.UpdatedFirstPointToChippingPoint() |
              animal_visited_location_domain.UpdateToSameLocationPoint() |
              animal_visited_location_domain.NextOfPreviousEqualThisLocation() | animal_domain.AnimalIsDead() |
              animal_visited_location_domain.LocationPointEqualToChippingLocation() |
              animal_visited_location_domain.AnimalNowInThisPoint() |
              animal_domain.ChippingLocationEqualFirstLocation() | animal_domain.AttemptToResurrectAnimal() |
              animal.AnimalHaveVisitedLocation() | type_of_specific_animal_domain.AnimalOnlyHasThisType()):
            return JSONResponse(status_code=400, content={'message': err.message()})
        case (animal.AnimalNotFound() | animal_type.AnimalTypeNotFound() | location_point.PointNotFound() |
              account.AccountNotFoundByID() | type_of_specific_animal_domain.AnimalNotHaveThisType() |
              animal_visited_location_domain.AnimalHasNoCurrentVisitedLocation() |
              animal_visited_location.AnimalVisitedLocationNotFound()):
            return JSONResponse(status_code=404, content={'message': err.message()})
        case (animal.AnimalHaveDuplicateTypes() | type_of_specific_animal_domain.AnimalAlreadyHaveThisType() |
              type_of_specific_animal_domain.AnimalAlreadyHaveThisTypes()):
            return JSONResponse(status_code=409, content={'message': err.message()})
