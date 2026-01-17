from typing import Any, Dict, List, Optional

from src.base_client import BaseClient


def search_bookings(
    client: BaseClient,
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    checkin: Optional[str] = None,
    checkout: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """GET /booking with query params and return results."""
    raise NotImplementedError("TODO: implement search_bookings")


def assert_booking_schema(booking: Dict[str, Any]) -> None:
    """Validate required fields for a booking."""
    raise NotImplementedError("TODO: implement assert_booking_schema")


def safe_get_booking(client: BaseClient, booking_id: int) -> Dict[str, Any]:
    """GET /booking/{booking_id} and raise on non-200."""
    raise NotImplementedError("TODO: implement safe_get_booking")


def main() -> None:
    client = BaseClient()
    results = search_bookings(client, firstname="Jim")
    print(f"Found {len(results)} matching bookings")

    if results:
        booking_id = results[0].get("bookingid")
        if isinstance(booking_id, int):
            booking = safe_get_booking(client, booking_id=booking_id)
            assert_booking_schema(booking)


if __name__ == "__main__":
    main()
