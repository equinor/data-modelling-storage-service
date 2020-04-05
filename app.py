import connexion
from api.config import Config


def create_app(config):
    connexion_app = connexion.App(__name__, specification_dir='./openapi/')

    flask_app = connexion_app.app
    flask_app.config.from_object(config)

    connexion_app.add_api(
        'api.yaml',
        arguments={'title': 'Data Modelling Storage Service API'},
        pythonic_params=True
    )

    return connexion_app.app


if __name__ == "__main__":
    app = create_app(Config)
    app.run(port=5000)
