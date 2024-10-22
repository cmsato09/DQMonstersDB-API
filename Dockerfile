FROM python:3.11

WORKDIR /project

COPY requirements.txt .

RUN pip install --no-cache-dir -r /project/requirements.txt

COPY src /project/src

ENV PYTHONPATH=/project

RUN python src/app/create_database.py

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--proxy-headers", "--port", "80"]
