FROM python:3.10-slim as base
WORKDIR /code
SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["/code/init.sh"]
CMD ["api"]
EXPOSE 5000

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code
ENV PATH="/code/.venv/bin:$PATH"

ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

COPY pyproject.toml /code/pyproject.toml
COPY poetry.lock /code/poetry.lock
COPY pyproject.toml ./
COPY pyproject.toml .
COPY pyproject.toml pyproject.toml



# Install poetry separated from system interpreter
RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

#RUN pip install --upgrade pip && \
#    pip install poetry && \
#    poetry config virtualenvs.in-project true
#RUN python -m venv .venv
#RUN source .venv/bin/activate

COPY poetry.lock pyproject.toml ./


FROM base as development
RUN poetry install
COPY .flake8 .behaverc ./
COPY src .

FROM base as prod
RUN poetry install --no-dev
COPY src .
