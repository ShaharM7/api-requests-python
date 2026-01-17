from typing import Any, Dict, List

from src.base_client import BaseClient


def health_check(client: BaseClient) -> None:
    """GET /ping and assert service is healthy."""
    raise NotImplementedError("TODO: implement health_check")


def list_booking_ids(client: BaseClient) -> List[int]:
    """GET /booking and return a list of booking IDs."""
    raise NotImplementedError("TODO: implement list_booking_ids")


def get_booking(client: BaseClient, booking_id: int) -> Dict[str, Any]:
    """GET /booking/{booking_id} and return the booking."""
    raise NotImplementedError("TODO: implement get_booking")


def create_booking(client: BaseClient, payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST /booking and return the create response."""
    raise NotImplementedError("TODO: implement create_booking")


def main() -> None:
    client = BaseClient()

    health_check(client)
    booking_ids = list_booking_ids(client)
    print(f"Retrieved {len(booking_ids)} booking IDs")

    if booking_ids:
        booking = get_booking(client, booking_id=booking_ids[0])
        print(f"First booking firstname: {booking.get('firstname')}")

    created = create_booking(
        client,
        payload={
            "firstname": "Jane",
            "lastname": "Doe",
            "totalprice": 123,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-05"},
            "additionalneeds": "Breakfast",
        },
    )
    print(f"Created booking id: {created.get('bookingid')}")


if __name__ == "__main__":
    main()
