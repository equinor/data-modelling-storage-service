import connexion

from api.config import Config
from api.utils.logging import logger


def create_app(config):

    if not Config.AUTH_ENABLED:
        logger.warning("Authentication is DISABLED. This deployment should only be reachable locally.")
    else:
        logger.info("Authentication enabled. Configuration;")
        logger.info(f"AUTH_JWK_URL: {Config.AUTH_JWK_URL}")
        logger.info(f"AUTH_JWT_AUDIENCE: {Config.AUTH_JWT_AUDIENCE}")

    connexion_app = connexion.App(__name__, specification_dir="./openapi/")
    connexion_app.debug = bool(Config.FLASK_DEBUG)

    flask_app = connexion_app.app
    flask_app.config.from_object(config)

    connexion_app.add_api("api.yaml", arguments={"title": "Data Modelling Storage Service API"}, pythonic_params=True)

    return connexion_app.app


if __name__ == "__main__":
    app = create_app(Config)
    app.run(port=5000)
