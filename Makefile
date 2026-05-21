run:
	uvicorn src.main:app
revision:
	alembic revision --autogenerate
upgrade:
	alembic upgrade head
t:
	python -m src.utils.teststand
