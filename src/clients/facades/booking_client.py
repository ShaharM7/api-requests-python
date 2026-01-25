import logging
import json

from src.clients.abstract_base_client import AbstractBaseClient
from src.models.booking.bookings_models import BookingModel, BookingResponse
from src.models.http_response import HttpResponse


class BookingClient:
    """
    High-level booking API (Facade Pattern).
    Hides HTTP complexity from tests.
    """ 

    def __init__(self, client: AbstractBaseClient) -> None:
        self.client = client
        self.booking_endpoint = "/booking"

    def create_booking(self, booking_model: BookingModel) -> BookingResponse:
        logging.info(f"Creating booking:\n{booking_model.model_dump_json(indent=2)}")

        http_response: HttpResponse = self.client.post(endpoint=self.booking_endpoint,
                        payload=booking_model.model_dump(mode="json"))

        # Replace manual check with raise_for_status()
        http_response.raise_for_status()  # ← Raises exception if 4xx/5xx

        return BookingResponse(**http_response.json())

    def get_booking(self, booking_id: str) -> BookingModel:
        logging.info(f"Get Booing Id:\n{booking_id}")
        
        get_endpoint = f"{self.booking_endpoint}/{booking_id}"
        http_response: HttpResponse = self.client.get(endpoint=get_endpoint)
    
        http_response.raise_for_status()  # ← Cleaner than manual check

        return BookingModel(**http_response.json())

    def create_booking_raw(self, booking_dict: dict) -> HttpResponse:
        """Create booking with raw dict (for negative testing)"""
        return self.client.post(
                endpoint=self.booking_endpoint,
                payload=booking_dict
            )

    def get_all_booking_ids(self) -> list[int]: 
        logging.info(f"Get All List Booing Ids:")
        http_response: HttpResponse = self.client.get(endpoint=self.booking_endpoint)
        http_response.raise_for_status()  # ← Cleaner than manual check

        return [item["bookingid"] for item in http_response.json()]

    def get_booking_ids_by_filter(self, filters: BookingModel) -> list[int]:
        params = None
        if filters:
            params = filters.model_dump(mode="json", exclude_none=True)
        
        http_response: HttpResponse = self.client.get(
            endpoint=self.booking_endpoint,
            params=params
        )
        http_response.raise_for_status()
        
        return [item["bookingid"] for item in http_response.json()]