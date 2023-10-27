FROM python:3.12-slim as base
WORKDIR /code
ENTRYPOINT ["/code/src/init.sh"]
CMD ["api"]
EXPOSE 5000

ENV PATH="/code/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code/src

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.in-project true

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

FROM base as development
RUN poetry install
COPY /src/.behaverc ./src/.behaverc
COPY src ./src
RUN chown -R 1000:1000 /code/src/home/system/data_sources/system.json
USER 1000

FROM base as prod
RUN poetry install --no-dev
COPY src ./src
RUN chown -R 1000:1000 /code/src/home/system/data_sources/system.json
USER 1000