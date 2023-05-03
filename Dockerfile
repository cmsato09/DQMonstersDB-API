FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]