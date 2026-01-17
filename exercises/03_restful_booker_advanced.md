# 03 - Restful Booker Advanced Practice

Goal: build filtering, negative cases, and validation helpers.

Setup:
- Set `BASE_URL` to `https://restful-booker.herokuapp.com`.
- Copy template `exercises/templates/restful_booker_advanced.py` to
  `src/practice/restful_booker_advanced.py`.

Tasks:
1. Implement `search_bookings` with query params:
   - `firstname`, `lastname`, `checkin`, `checkout`.
2. Implement `assert_booking_schema` to validate required fields.
3. Implement `safe_get_booking` that raises a clear error for non-200.

Stretch ideas:
- Add a function that compares two bookings and reports field diffs.
- Add a paging-like helper that splits large results into chunks.
