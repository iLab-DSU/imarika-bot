# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for PDF processing, JSON parsing (jq), and other libraries
RUN apt-get update && apt-get install -y \
    ghostscript \
    git \
    build-essential \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies (includes requests and python-dotenv)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
# This includes streamlit_app.py, rag_agent.py, and the data directory
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
