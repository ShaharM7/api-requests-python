# 03 - Gmail-Style Practice

Goal: model a Gmail-like workflow (messages, labels) with a small client
class.

Setup:
- Point `BASE_URL` to your Gmail-style API or a mock server.
- Copy template `exercises/templates/gmail_like_client.py` to
  `src/practice/gmail_like_client.py`.

Suggested endpoints (adjust to your API):
- `GET /messages` -> list messages (accepts query params like `q` or `label`)
- `GET /messages/{message_id}` -> fetch a single message
- `POST /messages/send` -> send a message
- `POST /labels` -> create a label
- `POST /messages/{message_id}/modify` -> add/remove labels
- `DELETE /messages/{message_id}` -> delete a message

Tasks:
1. Implement the client methods to hit these endpoints.
2. Create a label, send a message, and apply the label.
3. Fetch the message and confirm label state.

Stretch ideas:
- Add pagination support when listing messages.
- Add a safe delete helper that archives instead of deletes.
