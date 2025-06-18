# Build do projeto
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./

RUN poetry install --without dev --no-root --no-interaction --no-ansi

COPY ./app ./app

EXPOSE 8000

# Inicialização
CMD [ "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]