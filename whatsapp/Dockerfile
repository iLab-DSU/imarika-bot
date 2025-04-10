FROM python:latest

WORKDIR /app

COPY . .

EXPOSE 8080

CMD ["uvicorn", "server.whatsapp_api:app", "--host", "0.0.0.0", "--port", "8080"]