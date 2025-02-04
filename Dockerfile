# Use Playwright base image
FROM mcr.microsoft.com/playwright/python:v1.50.0-jammy

# Set environment variables for Poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies (excluding dev dependencies)
RUN poetry install --no-root 

# Copy application files
COPY . .

# Expose FastAPI's default port
EXPOSE 8080

# Command to start FastAPI server
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
