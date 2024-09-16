FROM python:3.11-slim

WORKDIR /Backend

COPY requirements.txt .

RUN python -m pip install --upgrade pip\
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]