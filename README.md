# API Requests Practice (Python)

Small `requests` wrapper and practice exercises to build API skills with the
Restful Booker API.

## Quick start
1. Create and activate a virtual environment.
2. Install deps: `pip install -r requirements.txt`.
3. Create `.env` at repo root:
   - `BASE_URL=https://restful-booker.herokuapp.com`
   - `API_USERNAME=admin`
   - `API_PASSWORD=password123`
4. Run tests with `pytest` (requires valid API credentials).

Note: the auth fixture uses `API_USERNAME` and `API_PASSWORD` for `/auth`.

## Practice exercises
See `exercises/README.md` for step-by-step practice and templates.

## Structure
- `src/base_client.py`: HTTP wrapper used by all exercises.
- `tests/`: pytest config and fixtures.
- `exercises/`: practice prompts and templates.
