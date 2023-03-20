from .common import location_point_exception_handler

from .get_controllers import location_point_router
from .post_controllers import location_point_router
from .put_controllers import location_point_router
from .delete_controllers import location_point_router

__all__ = ['location_point_router', 'location_point_exception_handler']
