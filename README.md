# hiring-funnel-analyzer
Описание: платформа аналитики воронки найма с ML-прогнозом оффера, SHAP-объяснениями, интеграцией с ATS (Greenhouse/Lever), дашбордом и REST API.  Стек: Python 3.11, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Celery, Redis, scikit-learn, SHAP, Streamlit, Docker, GitHub Actions.


# hiring-funnel-analyzer

Платформа аналитики воронки найма с ML-прогнозом оффера.

## Функции
- Хранение кандидатов и стадий
- REST API для ATS-интеграций (Greenhouse, Lever)
- ML-модель предсказания вероятности оффера
- SHAP-объяснение каждого прогноза
- Дашборд аналитика воронки
- Фоновые задачи синхронизации

## Быстрый старт

git clone https://github.com/your-org/hiring-funnel-analyzer
cd hiring-funnel-analyzer
cp .env.example .env
docker-compose up --build

API: http://localhost:8000/docs
Dashboard: http://localhost:8501

## Локальный запуск

make dev
make migrate
make seed
make run

## Обучение модели

python -m app.ml.train --data data/candidates.csv --out app/ml/model.pkl

## Тесты

make test

## API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | /api/candidates | создать кандидата |
| GET | /api/candidates | список кандидатов |
| GET | /api/stages/funnel | воронка |
| GET | /api/predictions/{id} | прогноз + SHAP |
| POST | /api/sync/{provider} | запуск синхронизации |

## Лицензия
MIT
