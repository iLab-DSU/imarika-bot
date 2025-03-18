# Advanced AI Bot with LangChain

This project is an advanced AI bot built with LangChain. It uses a JSON-based vector database, manages conversation logs and user data in a Postgres database (with async support and Alembic migrations), and handles real-time interactions via a FastAPI WebSocket server. The bot leverages Ollama models (via API) and is accessed through a Streamlit UI.

## Features

- **Modular design:** Separates UI, chain logic, server endpoints, and database management.
- **Advanced asynchronous support:** Uses async/await for database operations and WebSocket communication.
- **Structured logging:** Logs events and errors directly to a Postgres DB.
- **Containerized deployment:** Docker Compose orchestrates Postgres, Ollama, and the WebSocket server.
- **Database migrations:** Managed with Alembic for smooth schema evolution.

## Setup

1. Configure environment variables in the `.env` file.
2. Run `./scripts/setup.sh` to set up your local development environment.
3. Deploy the entire stack using `./scripts/deploy.sh`.

## License

MIT License
