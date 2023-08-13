set -x

poetry run ruff .
poetry run isort .
poetry run mypy .
