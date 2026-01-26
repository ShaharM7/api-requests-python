import json
import logging

from src.clients.abstract_base_client import AbstractBaseClient
from src.models.booking.bookings_models import BookingModel, BookingResponse, BookingRequest
from src.models.http_response import HttpResponse


class BookingClient:
    """
    High-level booking API (Facade Pattern).
    Hides HTTP complexity from tests.
    """

    def __init__(self, client: AbstractBaseClient) -> None:
        self.client = client
        self.booking_endpoint = "/booking"

    # ============ Create METHODS ============

    def create_booking(self, booking_model: BookingModel) -> BookingResponse:
        logging.info(f"Creating booking:\n{booking_model.model_dump_json(indent=2)}")

        http_response: HttpResponse = self.client.post(endpoint=self.booking_endpoint,
                                                       payload=booking_model.model_dump(mode="json"))

        # Replace manual check with raise_for_status()
        http_response.raise_for_status()  # ← Raises exception if 4xx/5xx

        booking_response = BookingResponse(**http_response.json())
        logging.info(f"Booking Id: {str(booking_response.bookingid)} Created")
        return booking_response

    def create_booking_raw(self, booking_dict: dict) -> HttpResponse:
        """Create booking with raw dict (for negative testing)"""
        return self.client.post(
            endpoint=self.booking_endpoint,
            payload=booking_dict
        )

    # ============ Get METHODS ============

    def get_booking(self, booking_id: str) -> BookingModel:
        logging.info(f"Get Booing Id:\n{booking_id}")

        get_endpoint = f"{self.booking_endpoint}/{booking_id}"
        http_response: HttpResponse = self.client.get(endpoint=get_endpoint)

        http_response.raise_for_status()  # ← Cleaner than manual check

        return BookingModel(**http_response.json())

    def get_all_booking_ids(self) -> list[int]:
        logging.info(f"Get All List Booing Ids:")
        http_response: HttpResponse = self.client.get(endpoint=self.booking_endpoint)
        http_response.raise_for_status()  # ← Cleaner than manual check

        return [item["bookingid"] for item in http_response.json()]

    def get_booking_ids_by_filter(self, filters: BookingRequest) -> list[int]:
        params = None
        if filters:
            params = filters.model_dump(mode="json", exclude_none=True)

        http_response: HttpResponse = self.client.get(
            endpoint=self.booking_endpoint,
            params=params
        )
        http_response.raise_for_status()

        return [item["bookingid"] for item in http_response.json()]

    # ============ UPDATE METHODS ============

    def update_booking(self, booking_id: int, booking_model: BookingModel) -> BookingModel:
        """Full update of a booking (PUT)"""
        logging.info(f"Updating booking {booking_id}:\n{booking_model.model_dump_json(indent=2)}")

        update_endpoint = f"{self.booking_endpoint}/{booking_id}"
        http_response: HttpResponse = self.client.put(
            endpoint=update_endpoint,
            payload=booking_model.model_dump(mode="json")
        )
        http_response.raise_for_status()

        return BookingModel(**http_response.json())

    def partial_update_booking(self, booking_id: int, updates: dict) -> BookingModel:
        """Partial update of a booking (PATCH)"""
        logging.info(f"Partial update booking {booking_id}:\n{json.dumps(updates, indent=2, default=str)}")

        patch_endpoint = f"{self.booking_endpoint}/{booking_id}"
        http_response: HttpResponse = self.client.patch(
            endpoint=patch_endpoint,
            payload=updates
        )
        http_response.raise_for_status()

        return BookingModel(**http_response.json())

    def update_booking_raw(self, booking_id: int, payload: dict) -> HttpResponse:
        """Update booking with raw dict (for negative testing)"""
        update_endpoint = f"{self.booking_endpoint}/{booking_id}"
        return self.client.put(endpoint=update_endpoint, payload=payload)

    def partial_update_booking_raw(self, booking_id: int, payload: dict) -> HttpResponse:
        """Partial update booking with raw dict (for negative testing)"""
        patch_endpoint = f"{self.booking_endpoint}/{booking_id}"
        return self.client.patch(endpoint=patch_endpoint, payload=payload)

    # ============ DELETE METHODS ============

    def delete_booking(self, booking_id: int) -> HttpResponse:
        """Delete a booking"""
        logging.info(f"Deleting booking {booking_id}")

        delete_endpoint = f"{self.booking_endpoint}/{booking_id}"
        http_response: HttpResponse = self.client.delete(endpoint=delete_endpoint)
        http_response.raise_for_status()

        return http_response

    def delete_booking_raw(self, booking_id: int) -> HttpResponse:
        """Delete booking returning raw response (for negative testing)"""
        delete_endpoint = f"{self.booking_endpoint}/{booking_id}"
        return self.client.delete(endpoint=delete_endpoint)
