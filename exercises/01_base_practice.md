# 01 - Base HTTP Practice

Goal: get comfortable with GET and POST requests and basic response
validation against the Restful Booker API.

Setup:
- Set `BASE_URL` to `https://restful-booker.herokuapp.com`.
- Copy template `exercises/templates/base_practice.py` to
  `src/practice/base_practice.py`.

Tasks:
1. Implement `health_check` to GET `/ping` and assert a successful response.
2. Implement `list_booking_ids` to GET `/booking` and return booking IDs.
3. Implement `get_booking` to GET `/booking/{booking_id}`.
4. Implement `create_booking` to POST `/booking` with a JSON payload.

Validation hints:
- Assert `response.status_code` for success (note: `/ping` returns 201).
- Confirm `Content-Type` includes `application/json` for JSON responses.
- Validate expected fields in the JSON response (for example `bookingid`).

Stretch ideas:
- Add a default `timeout` to each request.
- Handle non-2xx responses with clear exceptions.
