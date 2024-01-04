FROM python:3.12-slim as base
WORKDIR /code
ENTRYPOINT ["/code/src/init.sh"]
CMD ["api"]
EXPOSE 5000

ENV PATH="/code/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code/src


# gettext package is needed for envsubst command used in init.sh
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y gettext

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.in-project true

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

FROM base as development
RUN poetry install
COPY /src/.behaverc ./src/.behaverc
COPY src ./src
USER 1000

FROM base as prod
RUN poetry install --no-dev
COPY src ./src
USER 1000