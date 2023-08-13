set -x

poetry run pytest tests/ && poetry run pytest --cov=ram_machine/ tests/
