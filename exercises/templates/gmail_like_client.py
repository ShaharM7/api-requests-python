from typing import Any, Dict, List, Optional

from src.base_client import BaseClient


class GmailLikeClient:
    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def list_messages(
        self, query: Optional[str] = None, label: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """GET /messages with optional query params."""
        raise NotImplementedError("TODO: implement list_messages")

    def get_message(self, message_id: str) -> Dict[str, Any]:
        """GET /messages/{message_id}."""
        raise NotImplementedError("TODO: implement get_message")

    def send_message(self, to_email: str, subject: str, body: str) -> Dict[str, Any]:
        """POST /messages/send with {"to": ..., "subject": ..., "body": ...}."""
        raise NotImplementedError("TODO: implement send_message")

    def create_label(self, name: str) -> Dict[str, Any]:
        """POST /labels with {"name": name}."""
        raise NotImplementedError("TODO: implement create_label")

    def modify_message_labels(
        self,
        message_id: str,
        add_labels: List[str],
        remove_labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """POST /messages/{message_id}/modify with label changes."""
        raise NotImplementedError("TODO: implement modify_message_labels")

    def delete_message(self, message_id: str) -> None:
        """DELETE /messages/{message_id}."""
        raise NotImplementedError("TODO: implement delete_message")
