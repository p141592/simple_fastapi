# Repository Guidelines

## Project Structure & Module Organization
Core application code lives under `project/`. Use `project/core/` for app setup, settings, database wiring, and service endpoints such as health and metrics. Feature code belongs in `project/apps/`; the current example is `project/apps/user/` with `models.py`, `serializers.py`, and `views.py`. Static assets and templates are served from `project/static/`, `project/media/`, and `project/templates/`. Alembic migrations live in `migrations/`. Tests mirror the runtime structure under `tests/` (`tests/test_core/`, `tests/test_utils/`).

## Build, Test, and Development Commands
Install dependencies with `make activate` or `poetry install --no-root`. Run the app locally with `make run`; this starts `uvicorn project.asgi:app --reload` with `PYTHONPATH=$(pwd)/project`. Run the full test suite with `make test`. Run formatting checks with `make linter` (`black .`). Create and apply schema changes with `make makemigrations` and `make migrate`. Build the container with `make build`.

## Coding Style & Naming Conventions
Target Python 3.8 and follow Black formatting defaults: 4-space indentation, double quotes where Black chooses them, and imports grouped by standard library, third-party, then local modules. Keep module names lowercase with underscores, class names in `PascalCase`, and functions, variables, and route handlers in `snake_case`. Follow the existing app layout when adding features: `models.py`, `serializers.py`, `views.py`, then register routes in `project/apps/routes.py`.

## Testing Guidelines
Tests use `pytest`, `pytest-asyncio`, and `pytest-cov`. Name files `test_*.py` and keep test classes and functions descriptive, for example `TestApplication.test_ping`. `make test` runs coverage for `project/` and emits terminal plus XML reports. The shared `client` fixture in `tests/conftest.py` migrates the database up and down per test, so keep PostgreSQL available locally before running tests.

## Commit & Pull Request Guidelines
Recent history favors short, imperative commit subjects such as `update`, `deps`, and `lock`; more descriptive messages are better when changing behavior, for example `Add user delete validation`. Keep commits focused and avoid mixing dependency locks with feature work unless required. PRs should include a short summary, note any migration or config changes, link the issue when applicable, and include request/response examples or screenshots when API or UI behavior changes.

## Environment & Configuration Tips
Settings are defined in `project/core/settings.py` and loaded from `project/.env`. Set `DB_DSN` explicitly if you are not using the default local Postgres connection. Most commands rely on `PYTHONPATH=$(pwd)/project`; use the Make targets rather than invoking tools manually unless you need custom arguments.
