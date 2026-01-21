from src.clients.abstract_base_client import AbstractBaseClient


class BookingClient:
    """
    High-level booking API (Facade Pattern).
    Hides HTTP complexity from tests.
    """ 

    def __init__(self, client: AbstractBaseClient) -> None:
        self.client = client
        self.booking_endpoint = "/booking"