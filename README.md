# API Requests Practice (Python)

Small `requests` wrapper and practice exercises to build API skills (base
flows plus Trello/Gmail-style flows).

## Quick start
1. Create and activate a virtual environment.
2. Install deps: `pip install -r requirements.txt`.
3. Create `.env` at repo root:
   - `BASE_URL=https://example.com`
   - `API_PASSWORD=your-secret`
4. Run tests with `pytest` (requires valid API credentials).

Note: the current auth fixture uses `API_PASSWORD` as both username and
password. Update `tests/conftest.py` if your API expects separate values.

## Practice exercises
See `exercises/README.md` for step-by-step practice and templates.

## Structure
- `src/base_client.py`: HTTP wrapper used by all exercises.
- `tests/`: pytest config and fixtures.
- `exercises/`: practice prompts and templates.
