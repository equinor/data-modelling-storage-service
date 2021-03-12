FROM python:3.8-slim as base
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
CMD /usr/src/app/api/init.sh
EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=/usr/src/app/app.py
ENV PYTHONPATH=/usr/src/app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

FROM base as development
RUN poetry install
# Install API
COPY requirements.txt requirements.txt
COPY gen gen
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

FROM base as prod
# Install API
COPY requirements.txt requirements.txt
COPY gen gen
RUN poetry install --no-dev
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

