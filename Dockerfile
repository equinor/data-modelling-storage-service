FROM python:3.10-slim as base
WORKDIR /project
ENTRYPOINT ["/project/src/init.sh"]
CMD ["api"]
EXPOSE 5000

ENV PATH="/project/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/project/src

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.in-project true

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

FROM base as development
RUN poetry install
COPY .flake8 .behaverc ./
COPY src ./src
USER 1000

FROM base as prod
RUN poetry install --no-dev
COPY src ./src
USER 1000