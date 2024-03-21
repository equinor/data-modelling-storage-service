# Data Modelling Storage Service

![Checks](https://github.com/equinor/data-modelling-storage-service/actions/workflows/on-master-push.yml/badge.svg)
[![SCM Compliance](https://scm-compliance-api.radix.equinor.com/repos/equinor/data-modelling-storage-service/badge)](https://scm-compliance-api.radix.equinor.com/repos/equinor/data-modelling-storage-service/badge)


Backend service for the [Marine Analysis Framework](https://equinor.github.io/dm-docs/)

For documentation, usage, and guides regarding the framework, visit [https://equinor.github.io/dm-docs/](https://equinor.github.io/dm-docs/)

## Development

### Prerequisites

In order to run the commands described below, you need:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Running

```bash
$ docker compose up
```

### Testing

Running integration tests:

```bash
$ docker compose run --rm dmss behave
```

Run BDD tests by regexp:

```bash
$ docker compose run --rm dmss behave -n "Scenario name" # Run single test
```

Run unit tests:

```bash
$ docker compose run --rm dmss pytest
```

## Contributing
If you would like to contribute, please read our [Contribution guide](https://equinor.github.io/dm-docs/contributing/).
