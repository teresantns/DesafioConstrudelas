FROM python:3.9.1-slim

WORKDIR /app

COPY requirements.txt .
RUN  pip3 install -r requirements.txt

COPY . .

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]