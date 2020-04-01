# Data Modelling Storage Service

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

API documentation will be available at [localhost:8000/api/v1/ui/](http://localhost:8000/api/v1/ui/).

To refresh database after running 
```
docker-compose exec mainapi ./api/reset-database.sh
```

## Testing

BDD tests:

```
docker-compose run --rm mainapi behave
```
