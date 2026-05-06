from typing import TYPE_CHECKING, Unpack

from breezeway.models.base import Paginated
from breezeway.models.reservation import Reservation
from breezeway.resources.reservation import ReservationListDict

if TYPE_CHECKING:
    from breezeway.breezeway import BreezewayClient, AsyncBreezewayClient


class ReservationClient:
    def __init__(self, client: BreezewayClient):
        self._client = client

    def list_page(self, **kwargs: Unpack[ReservationListDict]) -> Paginated[Reservation]:
        request = self._client.resource.reservation.list_reservations(**kwargs)
        reservations = self._client.process_request(request)
        return Paginated[Reservation].model_validate(reservations)

    def get(self, reservation_id: int) -> Reservation:
        request = self._client.resource.reservation.retrieve_reservation(reservation_id=reservation_id)
        reservation = self._client.process_request(request)
        return Reservation.model_validate(reservation)


class AsyncReservationClient:
    def __init__(self, client: AsyncBreezewayClient):
        self._client = client

    async def list_page(self, **kwargs: Unpack[ReservationListDict]) -> Paginated[Reservation]:
        request = self._client.resource.reservation.list_reservations(**kwargs)
        reservations = await self._client.process_request(request)
        return Paginated[Reservation].model_validate(reservations)

    async def get(self, reservation_id: int) -> Reservation:
        request = self._client.resource.reservation.retrieve_reservation(reservation_id=reservation_id)
        reservation = await self._client.process_request(request)
        return Reservation.model_validate(reservation)
