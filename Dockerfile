FROM python:3-alpine as development
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install API
COPY requirements.txt requirements.txt
COPY gen gen
RUN pip3 install --no-cache-dir -r requirements.txt

# Install dependencies
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=/usr/src/app/app.py
ENV PYTHONPATH=/usr/src/app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN apk update && \
    # Needed to compile a poetry dependecy(cryptography)
    apk add  gcc musl-dev python3-dev libffi-dev openssl-dev && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY . /usr/src/app
RUN cd api && poetry install

CMD /usr/src/app/api/init.sh
EXPOSE 8000


FROM development as prod
RUN poetry install --no-dev
# ENTRYPOINT ["python3"]
# CMD ["-m", "dmss_api"]

