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

```bash
./generate-python-package.sh # You need to generate the API before starting the service
docker-compose build
docker-compose up
```

API documentation can be found at [http://localhost:8000/docs](http://localhost:8000/docs).

### Database

To refresh the database after first-time:

```
docker-compose exec dmss ./reset-database.sh
```

## Available client APIs

To talk with the DMSS service, these clients are available:

* Python https://pypi.org/project/dmss-api/

## Development 

### Pre-commit

The project provides a `.pre-commit-config.yaml`-file that is used to setup git _pre-commit hooks_.

Alternative pre-commit installations can be found [here](https://pre-commit.com/#install).

#### 1) Install pre-commit

Optionally create a virtualenv (recommended)

```shell script
pip install pre-commit
pre-commit install
```

### 2) Install virtual environment 

Virtual environment is used for running unit tests with pre-commit. 

```bash
python -m venv .venv
source .venv/bin/activate
poetry install
```

### Testing

Run BDD tests:

```
docker-compose run --rm dmss behave
```

Run BDD tests by regexp:

```
docker-compose run --rm dmss behave -n "Scenario name" # Run single test  
```

Run unit tests:

```
docker-compose run --rm dmss pytest api
```


