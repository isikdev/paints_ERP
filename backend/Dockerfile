FROM python:3.12-slim

RUN apt update && \
    apt install -y postgresql-client
WORKDIR /backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY .env .env
COPY ./src ./src
WORKDIR /backend/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
