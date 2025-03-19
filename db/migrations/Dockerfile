FROM python:latest

# Set working directory
WORKDIR /app/migrations

# Install dependencies
RUN pip install --upgrade pip && \
    pip install sqlalchemy psycopg2-binary alembic python-dotenv

# Copy migration scripts and Alembic config
COPY . /app/migrations

# Ensure the correct working directory for Alembic
ENV ALEMBIC_CONFIG=/app/migrations/alembic.ini

# Wait for Postgres to be ready before running migrations
CMD ["sh", "-c", "sleep 10 && alembic -c /app/migrations/alembic.ini upgrade head"]
