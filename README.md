# Data Modelling Storage Service

![](https://github.com/equinor/data-modelling-storage-service/workflows/Testing/badge.svg)

## Prerequisites

In order to run the commands described below, you need:
- [Docker](https://www.docker.com/) 
- [Docker Compose](https://docs.docker.com/compose/)
- make (`sudo apt-get install make` on Ubuntu)

## Running

```bash
./generate-api.sh # You need to generate the API before starting the service
docker-compose build
docker-compose up
```

API documentation can be found at [http://localhost:8000/api/v1/ui](http://localhost:8000/api/v1/ui).

### Refresh database 

```
docker-compose exec mainapi ./api/reset-database.sh
```

## Testing

Run BDD tests:

```
docker-compose run --rm mainapi behave
```

Run unit tests:

```
docker-compose run --rm mainapi pytest api
```

## Available APIs

* Python https://pypi.org/project/dmss-api/

