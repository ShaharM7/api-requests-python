from typing import Any, Dict, List, Optional

from src.base_client import BaseClient


class TrelloLikeClient:
    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def create_board(self, name: str) -> Dict[str, Any]:
        """POST /boards with {"name": name}."""
        raise NotImplementedError("TODO: implement create_board")

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """GET /boards/{board_id}."""
        raise NotImplementedError("TODO: implement get_board")

    def create_list(self, board_id: str, name: str) -> Dict[str, Any]:
        """POST /boards/{board_id}/lists with {"name": name}."""
        raise NotImplementedError("TODO: implement create_list")

    def create_card(
        self, list_id: str, name: str, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """POST /lists/{list_id}/cards with {"name": name, "desc": description}."""
        raise NotImplementedError("TODO: implement create_card")

    def get_cards(self, board_id: str) -> List[Dict[str, Any]]:
        """GET /boards/{board_id}/cards."""
        raise NotImplementedError("TODO: implement get_cards")

    def move_card(self, card_id: str, target_list_id: str) -> Dict[str, Any]:
        """POST /cards/{card_id}/move with {"listId": target_list_id}."""
        raise NotImplementedError("TODO: implement move_card")

    def archive_card(self, card_id: str) -> Dict[str, Any]:
        """POST /cards/{card_id}/archive."""
        raise NotImplementedError("TODO: implement archive_card")
