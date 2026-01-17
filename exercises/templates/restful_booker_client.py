from typing import Any, Dict, List, Optional

from src.base_client import BaseClient


class RestfulBookerClient:
    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def health_check(self) -> None:
        """GET /ping and assert service is healthy."""
        raise NotImplementedError("TODO: implement health_check")

    def create_token(self, username: str, password: str) -> str:
        """POST /auth with credentials and return token."""
        raise NotImplementedError("TODO: implement create_token")

    def set_token(self, token: str) -> None:
        """Store token as Cookie header."""
        self.client.headers.update({"Cookie": f"token={token}"})

    def list_bookings(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """GET /booking with optional query params."""
        raise NotImplementedError("TODO: implement list_bookings")

    def get_booking(self, booking_id: int) -> Dict[str, Any]:
        """GET /booking/{booking_id}."""
        raise NotImplementedError("TODO: implement get_booking")

    def create_booking(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST /booking and return the response."""
        raise NotImplementedError("TODO: implement create_booking")

    def update_booking(self, booking_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """PUT /booking/{booking_id} and return updated booking."""
        raise NotImplementedError("TODO: implement update_booking")

    def partial_update_booking(
        self, booking_id: int, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """PATCH /booking/{booking_id} and return updated booking."""
        raise NotImplementedError("TODO: implement partial_update_booking")

    def delete_booking(self, booking_id: int) -> None:
        """DELETE /booking/{booking_id}."""
        raise NotImplementedError("TODO: implement delete_booking")
