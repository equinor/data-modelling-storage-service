# Data Modelling Storage Service

![Checks](https://github.com/equinor/data-modelling-storage-service/workflows/Testing/badge.svg)

![Docker Registry](https://github.com/equinor/data-modelling-storage-service/workflows/Publish%20DMSS%20API%20to%20docker%20registry/badge.svg?branch=master)

![PyPI](https://github.com/equinor/data-modelling-storage-service/workflows/Publish%20DMSS%20API%20to%20PyPI/badge.svg)

## Prerequisites

In order to run the commands described below, you need:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- make (`sudo apt-get install make` on Ubuntu)

## Running

1. Copy the .env-template and name it .env with the command: `cp .env-template .env`
2. Generate a secret key. Repository secrets are encrypted at rest. Therefore, an encryption key is needed. 
    ```bash
    docker-compose build
    KEY=$(docker-compose run --rm dmss create-key)
    echo $KEY
    ```
3. Copy the secret key and paste it .env under the name `SECRET_KEY`
4. Run `docker compose up`


API documentation can be found at [http://localhost:5000/docs](http://localhost:5000/docs).

### Database

To refresh the database after first-time:

```bash
docker-compose run --rm dmss reset-app
```

## Available client APIs

To talk with the DMSS service, these clients are available:

- Python https://pypi.org/project/dmss-api/

## Development

### Pre-commit

The project provides a `.pre-commit-config.yaml`-file that is used to setup git _pre-commit hooks_.

Alternative pre-commit installations can be found [here](https://pre-commit.com/#install).


### 1) Install a Python virtual environment

Virtual environment is used for running unit tests with pre-commit.
Note: to be able to run unit tests with pre-commit, a virtual environment is needed.

From the repository root folder, run the following commands:
```bash
python -m venv .venv
source .venv/bin/activate
poetry install
```

#### 2) Install pre-commit

From the repository root folder, after virtual environment is activated, run the following commands:
```shell script
pip install pre-commit
pre-commit install
```


### Testing

Run BDD tests:

```bash
docker-compose run --rm dmss behave
```

Run BDD tests by regexp:

```bash
docker-compose run --rm dmss behave -n "Scenario name" # Run single test
```

Run unit tests:

```bash
docker-compose run --rm dmss pytest api
```

Creating DMSS lookup with [dm-cli](https://github.com/equinor/dm-cli):

```bash
dm create-lookup dmss system/SIMOS/recipe_links
```
