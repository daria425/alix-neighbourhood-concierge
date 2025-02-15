# Use Playwright base image
FROM mcr.microsoft.com/playwright/python:v1.50.0-jammy
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app


COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root 

COPY . .

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
