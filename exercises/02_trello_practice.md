# 02 - Trello-Style Practice

Goal: model a Trello-like workflow (boards, lists, cards) with a small
client class.

Setup:
- Point `BASE_URL` to your Trello-style API or a mock server.
- Copy template `exercises/templates/trello_like_client.py` to
  `src/practice/trello_like_client.py`.

Suggested endpoints (adjust to your API):
- `POST /boards` -> create a board
- `GET /boards/{board_id}` -> fetch board info
- `POST /boards/{board_id}/lists` -> create a list
- `POST /lists/{list_id}/cards` -> create a card
- `GET /boards/{board_id}/cards` -> list cards
- `POST /cards/{card_id}/move` -> move card to another list
- `POST /cards/{card_id}/archive` -> archive card

Tasks:
1. Implement the client methods to hit these endpoints.
2. Build a short flow: create board -> create list -> create card.
3. Move the card to another list and archive it.

Stretch ideas:
- Add request idempotency keys for retries.
- Add negative tests for invalid board IDs.
