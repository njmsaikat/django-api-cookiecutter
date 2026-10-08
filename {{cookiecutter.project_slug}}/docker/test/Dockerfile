FROM python:{{ cookiecutter.python_version }}-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

{% if cookiecutter.use_celery == "y" %}# postgresql-client provides pg_dump for the scheduled database backup
RUN apt-get update && apt-get install --no-install-recommends -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*
{% endif %}
WORKDIR /app
COPY ./backend/requirements/ /app/backend/requirements/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements/test.txt

COPY ./docker/ /app/docker
COPY ./backend/ /app/backend

EXPOSE {{ cookiecutter.port }}
