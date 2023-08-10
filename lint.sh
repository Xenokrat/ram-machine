set -x

poetry run ruff .
poetry run isort .
poetry run pytest tests/ && poetry run pytest --cov=ram_machine/ tests/
