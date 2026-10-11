.PHONY: install dev test lint run worker dashboard seed migrate

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest tests/ -v

lint:
	ruff check app tests

run:
	uvicorn app.main:app --reload

worker:
	celery -A app.worker.celery worker -l info

dashboard:
	streamlit run dashboard/app.py

seed:
	python scripts/seed_data.py

migrate:
	alembic upgrade head
