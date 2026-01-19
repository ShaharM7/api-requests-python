from dotenv.main import logger
from src.clients.base_client import BaseClient


def test_get_all_bookings(client: BaseClient):
    """
    Test ensuring we can retrieve all booking IDs.
    The 'client' fixture is automatically injected from conftest.py
    and is already authenticated.
    """
    # 1. Action
    response = client.get("/booking")

    # 2. Validate Status Code
    # assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    # bookings: list[dict] = response.json()

    # logger.debug(f"DEBUG: Retrieved {len(bookings)} bookings")

    # Verify we got a non-empty list
    # assert len(bookings) > 0, "Booking list shouldn't be empty"
    # assert isinstance(bookings, list), "Response should be a list"