FROM postgres:13

# Use environment variables for database credentials
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=ai_bot

# Copy initialization script if needed
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the Postgres port
EXPOSE 5432
