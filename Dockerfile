FROM python:3.9-slim as base
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
CMD /usr/src/app/api/init.sh
EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

FROM base as development
RUN poetry install
COPY . /usr/src/app

FROM base as prod
RUN poetry install --no-dev
COPY . /usr/src/app

