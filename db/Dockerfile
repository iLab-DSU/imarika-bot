# db/Dockerfile
FROM postgres:13

# Set environment variables for Postgres
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=ai_bot

# Optionally, copy initialization scripts into the image
COPY init.sql /docker-entrypoint-initdb.d/

# Expose port 5432 (default Postgres port)
EXPOSE 5432
