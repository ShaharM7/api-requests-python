# Practice Exercises

Recommended order:
1. `01_base_practice.md`
2. `02_restful_booker_practice.md`
3. `03_restful_booker_advanced.md`

Each exercise has a matching template in `exercises/templates/`.
Copy a template to `src/practice/` (create it) or work directly in the
template file if you prefer.

Template mapping:
- `01_base_practice.md` -> `templates/base_practice.py`
- `02_restful_booker_practice.md` -> `templates/restful_booker_client.py`
- `03_restful_booker_advanced.md` -> `templates/restful_booker_advanced.py`

General rules:
- Use `BaseClient` from `src/base_client.py`.
- Keep requests in small functions or client classes.
- Validate status codes and response shape.
