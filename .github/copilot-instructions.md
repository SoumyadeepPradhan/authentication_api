# Copilot Instructions for AI Agents

## Project Overview
- This is a FastAPI-based authentication API with modular structure for user registration, login, and JWT-based authentication.
- Major directories:
  - `core/`: Configuration, database setup, and security (JWT, password hashing).
  - `users/`: User models, schemas, services, and routes for registration and user info.
  - `auth/`: Authentication endpoints and token management.
- The entry point is `main.py`, which wires routers and middleware.

## Architecture & Data Flow
- Uses SQLAlchemy ORM for MySQL (see `core/database.py` and `core/config.py`).
- JWT authentication is enforced via Starlette's `AuthenticationMiddleware` and a custom backend (`core/security.py`).
- User registration and login are handled in `users/routes.py` and `auth/route.py` respectively.
- Tokens are created and validated using `python-jose` and `passlib` for password hashing.

## Developer Workflows
- To run locally: activate the virtual environment in `myvenv/` and use Uvicorn:
  ```powershell
  .\myvenv\Scripts\activate
  uvicorn main:app --reload --port 8090
  ```
- Database connection settings are loaded from a `.env` file (see `core/config.py`).
- To install dependencies:
  ```powershell
  pip install -r requirements.txt
  ```

## Project-Specific Patterns
- Routers are split for unauthenticated (`router`) and authenticated (`user_router`) user endpoints in `users/routes.py`.
- All DB access uses SQLAlchemy sessions from `core/database.py:get_db`.
- JWT payloads use the user's email as the `id` claim.
- Passwords are always hashed before storage (`core/security.py`).
- Error handling uses FastAPI's `HTTPException` with custom messages.

## Integration Points
- Relies on MySQL (connection string built in `core/config.py`).
- Expects environment variables for DB and JWT config.
- Uses `python-dotenv` for local development.

## Examples
- To add a new protected route, use `user_router` in `users/routes.py` and require `Depends(oauth2_scheme)`.
- To add a new model, define it in `users/models.py` and update DB via Alembic or manual migration.

---

For questions about conventions or unclear patterns, review `main.py`, `core/`, and the relevant router/service files for examples.
