# Dockerfile (at the project root)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set PYTHONPATH so that Python can find the 'app' package
ENV PYTHONPATH=/app

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies with Poetry in a non-virtualenv mode
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the entire project into the container
COPY . .

# Expose ports for the FastAPI and Streamlit apps
EXPOSE 8000 8501

# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "server.ws_server:app", "--host", "0.0.0.0", "--port", "8000"]
