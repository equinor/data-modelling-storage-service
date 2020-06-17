import connexion
from connexion import decorators
from connexion.problem import problem
from jsonschema import ValidationError

from api.config import Config
from api.utils.logging import logger


class RequestBodyValidator(decorators.validation.RequestBodyValidator):
    """
    This class overrides the default connexion RequestBodyValidator
    so that it returns the complete string representation of the
    error, rather than just returning the error message.

    For more information:
        - https://github.com/zalando/connexion/issues/558
        - https://connexion.readthedocs.io/en/latest/request.html
    """

    def validate_schema(self, data, url):
        if self.is_null_value_valid:
            return None

        try:
            self.validator.validate(data)
        except ValidationError as exception:
            logger.error(
                "{url} validation error: {error}".format(url=url, error=exception), extra={"validator": "body"},
            )
            return problem(400, "Bad Request", str(exception))

        return None


def create_app(config):
    connexion_app = connexion.App(__name__, specification_dir="./openapi/")
    connexion_app.debug = bool(Config.FLASK_DEBUG)

    flask_app = connexion_app.app
    flask_app.config.from_object(config)

    connexion_app.add_api(
        "api.yaml",
        arguments={"title": "Data Modelling Storage Service API"},
        pythonic_params=True,
        strict_validation=False,
        validator_map={"body": RequestBodyValidator},
    )

    return connexion_app.app


if __name__ == "__main__":
    app = create_app(Config)
    app.run(port=5000)
