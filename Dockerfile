FROM python:3.13-slim AS builder

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root

COPY timetable_bot/src/ src/

CMD ["poetry", "run", "python", "src/main.py"]