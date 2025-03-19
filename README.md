# AI Bot

This project is an AI bot built to utilize a **vector database**, manage conversation logs and user data in a **Postgres database** (with async support and Alembic migrations), and handles real-time interactions via a **FastAPI WebSocket server**. The bot leverages **Ollama models** (via API) and is accessed through a **Streamlit UI**.

## ✨ Features
- 🛠 Modular Architecture – Clean separation of UI, AI logic, API, and database.
- ⚡ Asynchronous Processing – Uses async/await for efficient database and WebSocket operations.
- 📜 Structured Logging – Logs interactions and errors into PostgreSQL.
- 🐳 Dockerized Deployment – Runs seamlessly with Docker Compose.
- 📅 Database Migrations – Managed with Alembic for version control.

## Setup with Docker Compose

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-repo/ai-bot.git
   cd ai-bot
   ```

2. **Configure environment variables**:
   - Copy variables to `.env`:
   - Update necessary values inside `.env` (e.g., database credentials, API keys).

3. **Start the services**:
   ```sh
   docker compose up -d
   ```
   This will spin up:
   - **PostgreSQL** (for conversation logs and user data)
   - **FastAPI WebSocket server** (handles real-time interactions)
   - **Ollama API** (for AI model inference)
   - **Streamlit UI** (user interface)

4. **Apply database migrations**:
   ```sh
   docker compose exec backend alembic upgrade head
   ```

5. **Access the application**:
   - **Streamlit UI**: [http://localhost:8501](http://localhost:8501)
   - **FastAPI WebSocket server**: [http://localhost:8000](http://localhost:8000)
   - **PostgreSQL (via Docker)**: `postgres://user:password@localhost:5432/db_name`

## Setting Up Pre-commit Hooks

To ensure code quality, we use **pre-commit hooks** to automatically format and lint the code before commits.

1. **Install dependencies** (if not already installed):
   ```sh
   poetry install
   ```

2. **Install pre-commit hooks**:
   ```sh
   poetry run pre-commit install
   ```

3. **Manually run pre-commit on all files**:
   ```sh
   poetry run pre-commit run --all-files
   ```

4. **Adding new hooks (optional)**:  
   Modify `.pre-commit-config.yaml` to include additional linters or formatters.

---

## Stopping & Restarting

To stop the containers:

```sh
docker compose down
```

To restart:

```sh
docker compose up -d
```

## License

MIT License