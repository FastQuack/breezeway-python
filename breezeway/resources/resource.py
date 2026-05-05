from .base import BaseResource
from .company import CompanyResource
from .task import TaskResource
from .reservation import ReservationResource
from .unit import UnitResource
from .user import UserResource


class Resource(BaseResource):

    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.company = CompanyResource(base_url)
        self.reservation = ReservationResource(base_url)
        self.task = TaskResource(base_url)
        self.unit = UnitResource(base_url)
        self.user = UserResource(base_url)