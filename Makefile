run:
	python -m src.main
revision:
	alembic revision --autogenerate
upgrade:
	alembic upgrade head
t:
	pytest -m integration
