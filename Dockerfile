FROM python:3.12

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3 -

COPY ./src/backend/ ./

RUN poetry install

ENV VIRTUAL_ENV=.venv

RUN python3.12 manage.py collectstatic --noinput
