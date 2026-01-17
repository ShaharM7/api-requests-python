# 01 - Base HTTP Practice

Goal: get comfortable with GET, POST, PUT, DELETE, query params, and
response validation.

Setup:
- Set `BASE_URL` to `https://jsonplaceholder.typicode.com` (no auth needed).
- Copy template `exercises/templates/base_practice.py` to
  `src/practice/base_practice.py`.

Tasks:
1. Implement `list_posts` to GET `/posts` and return the list.
2. Implement `get_post` to GET `/posts/{post_id}`.
3. Implement `create_post` to POST `/posts` with a JSON payload.
4. Implement `update_post` to PUT `/posts/{post_id}` with new data.
5. Implement `delete_post` to DELETE `/posts/{post_id}`.

Validation hints:
- Assert `response.status_code` for success.
- Confirm `Content-Type` includes `application/json`.
- Validate expected fields in the JSON response (for example `id` or `title`).

Stretch ideas:
- Add a default `timeout` to each request.
- Handle non-2xx responses with clear exceptions.
