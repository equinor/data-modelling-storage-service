import json
import time

import click
import uvicorn
from domain_classes.user import User
from fastapi import APIRouter, FastAPI, Security
from starlette.requests import Request
from starlette.types import Scope, Receive, Send
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from authentication.authentication import get_current_user
from config import config
from restful.request_types.create_data_source import DataSourceRequest
from storage.internal.data_source_repository import DataSourceRepository
from utils.encryption import generate_key
from utils.logging import logger
from utils.package_import import import_package
from utils.wipe_db import wipe_db
from utils.mock_token_generator import generate_mock_token

server_root = "/api"
version = "v1"
prefix = f"{server_root}/{version}"


class AuthHeaderHTTPMiddleware(BaseHTTPMiddleware):
    """
    From https://github.com/tiangolo/fastapi/issues/3027#issuecomment-811724832
    """

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        auth_header_present = "authorization" in [value[0].decode() for value in scope["headers"]]
        if not auth_header_present:
            self.__add_auth_header(scope=scope)
        request = Request(scope, receive=receive)
        response = await self.dispatch_func(request, self.call_next)
        await response(scope, receive, send)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        return await call_next(request)

    @classmethod
    def __add_auth_header(cls, scope: Scope):
        token = generate_mock_token()
        scope["headers"].append((b"authorization", b"Bearer " + token.encode()))


def create_app():
    from controllers import (
        blob_controller,
        blueprint_controller,
        datasource_controller,
        document_controller,
        explorer_controller,
        export_controller,
        package_controller,
        reference_controller,
        search_controller,
        whoami_controller,
        healtcheck_controller,
        access_control_controller,
        personal_access_token_controller,
    )

    public_routes = APIRouter()
    authenticated_routes = APIRouter()

    public_routes.include_router(healtcheck_controller.router)

    authenticated_routes.include_router(whoami_controller.router)
    authenticated_routes.include_router(blob_controller.router)
    authenticated_routes.include_router(datasource_controller.router)
    authenticated_routes.include_router(document_controller.router)
    authenticated_routes.include_router(export_controller.router)
    authenticated_routes.include_router(package_controller.router)
    authenticated_routes.include_router(search_controller.router)
    authenticated_routes.include_router(blueprint_controller.router)
    authenticated_routes.include_router(reference_controller.router)
    authenticated_routes.include_router(explorer_controller.router)
    authenticated_routes.include_router(access_control_controller.router)
    authenticated_routes.include_router(personal_access_token_controller.router)

    app = FastAPI(
        title="Data Modelling Storage Service",
        description="API for basic data modelling interaction",
        swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": True, "clientId": config.OAUTH_CLIENT_ID},
    )
    app.include_router(authenticated_routes, prefix=prefix, dependencies=[Security(get_current_user)])
    app.include_router(public_routes, prefix=prefix)

    app.add_middleware(AuthHeaderHTTPMiddleware)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        milliseconds = int(round(process_time * 1000))
        logger.debug(f"Took {milliseconds}ms to process request '{request.url.path}'")
        response.headers["X-Process-Time"] = str(process_time)
        return response

    return app


@click.group()
def cli():
    pass


@cli.command()
def run():
    try:
        with open("./version.txt") as version_file:
            print(f"VERSION: {version_file.read()}")
    except FileNotFoundError:
        pass
    uvicorn.run(
        "app:create_app",
        host="0.0.0.0",  # nosec
        port=5000,
        reload=config.ENVIRONMENT == "local",
        log_level=config.LOGGER_LEVEL.lower(),
    )


@cli.command()
def init_application():
    logger.info("IMPORTING CORE DOCUMENTS")
    # Running commands locally sets the user_context to "DMSS_ADMIN"
    user = User(**{"username": config.DMSS_ADMIN, "full_name": "Local Admin", "email": "admin@example.com"})
    import_package(f"{config.APPLICATION_HOME}/system/SIMOS", user, data_source=config.CORE_DATA_SOURCE, is_root=True)
    logger.debug("DONE")


@cli.command()
@click.argument("file")
def import_data_source(file):
    with open(file) as json_file:
        document = json.load(json_file)
        # Running commands locally sets the user_context to "DMSS_ADMIN"
        user = User(**{"username": config.DMSS_ADMIN, "full_name": "Local Admin", "email": "admin@example.com"})
        DataSourceRepository(user).create(document["name"], DataSourceRequest(**document))


@cli.command()
def nuke_db():
    logger.info("PURGING DATABASE")
    wipe_db()
    logger.debug("DONE")


@cli.command()
@click.pass_context
def reset_app(context):
    context.invoke(nuke_db)
    logger.info("CREATING SYSTEM DATA SOURCE")
    context.invoke(import_data_source, file="/code/home/system/data_sources/system.json")
    logger.debug("DONE")
    context.invoke(init_application)


@cli.command()
@click.pass_context
def create_key(context):
    key = context.invoke(generate_key)
    print(key)


if __name__ == "__main__":
    cli()
