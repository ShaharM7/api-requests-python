# 02 - Restful Booker CRUD Practice

Goal: build a small client class that handles auth and CRUD flows for
bookings.

Setup:
- Set `BASE_URL` to `https://restful-booker.herokuapp.com`.
- Set `API_USERNAME` and `API_PASSWORD`.
- Copy template `exercises/templates/restful_booker_client.py` to
  `src/practice/restful_booker_client.py`.

Tasks:
1. Implement `create_token` and store it using `set_token`.
2. Implement `create_booking` and capture the new `bookingid`.
3. Implement `update_booking` (PUT) and `partial_update_booking` (PATCH).
4. Implement `delete_booking` and assert it succeeds (usually 201).

Suggested flow:
1. Create token -> create booking -> update -> partial update -> delete.
2. After delete, try `get_booking` and confirm 404.

Stretch ideas:
- Add a helper that validates required booking fields.
- Add retries for transient 5xx responses.
