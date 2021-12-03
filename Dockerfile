FROM python:3.9.0

# Просим Python не писать .pyc файлы
ENV PYTHONDONTWRITEBYTECODE 1

# Просим Python не буферизовать stdin/stdout
ENV PYTHONUNBUFFERED 1

WORKDIR  /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
