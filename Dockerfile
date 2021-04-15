FROM python:3.9-slim as base
WORKDIR /code
CMD /code/init.sh
EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

FROM base as development
RUN poetry install
COPY .flake8 .behaverc ./
COPY src .

FROM base as prod
RUN poetry install --no-dev
COPY src .

