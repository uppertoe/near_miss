# Dockerfile with multi-stage build
ARG PYTHON_VERSION=3.10-slim-buster

# Stage 1: Install dependencies
FROM python:${PYTHON_VERSION} AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g \
    postcss-cli \
    autoprefixer \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

# Stage 2: Build the app
FROM build AS app

WORKDIR /code

COPY . /code/

RUN python manage.py collectstatic --noinput && \
    python manage.py compress --force

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "core.wsgi"]