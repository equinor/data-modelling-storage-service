import json
import time
from collections.abc import Callable
from datetime import datetime
from uuid import uuid4

import click
import gridfs
import uvicorn
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.storage.blob import BlobServiceClient
from fastapi import APIRouter, FastAPI, Security
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response

from authentication.authentication import auth_w_jwt_or_pat, auth_with_jwt
from authentication.models import User
from common.exceptions import ErrorResponse
from common.utils.encryption import generate_key
from common.utils.logging import logger
from common.utils.package_import import import_package
from config import config
from features.lookup_table.use_cases.create_lookup_table import (
    create_lookup_table_use_case,
)
from restful.request_types.create_data_source import DataSourceRequest
from services.database import mongo_client
from storage.internal.data_source_repository import DataSourceRepository

server_root = "/api"


def create_app() -> FastAPI:
    from features.access_control import access_control_feature
    from features.attribute import attribute_feature
    from features.blob import blob_feature
    from features.blueprint import blueprint_feature
    from features.datasource import datasource_feature
    from features.document import document_feature
    from features.entity import entity_feature
    from features.export import export_feature
    from features.file import file_feature
    from features.health_check import health_check_feature
    from features.lookup_table import lookup_table_feature
    from features.meta import meta_feature
    from features.personal_access_token import personal_access_token_feature
    from features.search import search_feature
    from features.whoami import whoami_feature

    public_routes = APIRouter()
    public_routes.include_router(health_check_feature.router)

    authenticated_routes = APIRouter()
    authenticated_routes.include_router(access_control_feature.router)
    authenticated_routes.include_router(blob_feature.router)
    authenticated_routes.include_router(blueprint_feature.router)
    authenticated_routes.include_router(datasource_feature.router)
    authenticated_routes.include_router(document_feature.router)
    authenticated_routes.include_router(export_feature.router)
    authenticated_routes.include_router(search_feature.router)
    authenticated_routes.include_router(whoami_feature.router)
    authenticated_routes.include_router(entity_feature.router)
    authenticated_routes.include_router(lookup_table_feature.router)
    authenticated_routes.include_router(attribute_feature.router)
    authenticated_routes.include_router(file_feature.router)
    authenticated_routes.include_router(meta_feature.router)

    # Some routes a PAT can not be used to authenticate. For example, to get new access tokens. That would be bad...
    jwt_only_routes = APIRouter()
    jwt_only_routes.include_router(personal_access_token_feature.router)

    app = FastAPI(
        title="Data Modelling Storage Service",
        version="1.22.0",  # x-release-please-version
        description="API for basic data modelling interaction",
        swagger_ui_init_oauth={
            "clientId": config.OAUTH_CLIENT_ID,
            "appName": "DMSS",
            "usePkceWithAuthorizationCodeGrant": True,
            "scopes": config.OAUTH_AUTH_SCOPE,
            "useBasicAuthenticationWithAccessCodeGrant": True,
        },
    )
    app.include_router(
        authenticated_routes,
        prefix=server_root,
        dependencies=[Security(auth_w_jwt_or_pat)],
    )
    app.include_router(jwt_only_routes, prefix=server_root, dependencies=[Security(auth_with_jwt)])
    app.include_router(public_routes, prefix=server_root)

    if config.ENVIRONMENT in ("local", "CI"):
        logger.warning("CORS has been turned off. This should only occur in in development.")
        # Turn off CORS when running locally. allow_origins argument can be replaced with a list of URLs.
        app.add_middleware(
            CORSMiddleware,
            allow_origins="*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    if config.APPINSIGHTS_BE_CONNECTION_STRING:
        configure_azure_monitor(connection_string=config.APPINSIGHTS_BE_CONNECTION_STRING, logger_name="API")
        FastAPIInstrumentor.instrument_app(app)

    # Intercept FastAPI builtin validation errors, so they can be returned on our standardized format.
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            ErrorResponse(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                type="RequestValidationError",
                message="The received values are invalid",
                debug="The received values are invalid according to the endpoints model definition",
                data=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
            ).dict(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        milliseconds = int(round(process_time * 1000))
        logger.info(f"{request.method} {request.url.path} - {milliseconds}ms - {response.status_code}")
        response.headers["X-Process-Time"] = str(process_time)
        request.state.request_time = process_time  # Make request_time available for subsequently middlewares
        return response

    if config.PROFILING_ENABLED:
        from pathlib import Path

        from fastapi import BackgroundTasks
        from pyinstrument import Profiler
        from pyinstrument.renderers.html import HTMLRenderer
        from pyinstrument.renderers.speedscope import SpeedscopeRenderer

        @app.middleware("http")
        async def profile_request(request: Request, call_next):
            """Profile the current request.

            Profile requests and store (to disk or Azure blob storage) a JSON report compatible with Speedscope
            or simple HTML report. See https://github.com/jlfwong/speedscope for how to install and use Speedscope.

            If used with docker image, mount the "/code/src/profiles" to the host for direct access to the performance profiles.

            Query params:
            - profile (bool): profile the request, default is false
            - profile_format (string): specify profile format (html or speedscope), default is speedscope
            - profile_time_limit (number): only store profiles if above given time limit (defined in seconds), default is to store everyhing
            """
            if request.query_params.get("profile", False):
                with Profiler(interval=0.001, async_mode="enabled") as profiler:
                    response = await call_next(request)

                profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
                profile_type_to_renderer = {
                    "html": HTMLRenderer,
                    "speedscope": SpeedscopeRenderer,
                }
                profile_type = request.query_params.get("profile_format", "speedscope")
                extension = profile_type_to_ext[profile_type]
                renderer = profile_type_to_renderer[profile_type]()
                request_time: float = getattr(request.state, "request_time", 0.0)
                file_name = f"{datetime.now().strftime("%Y-%m-%d")}-{config.ENVIRONMENT}-{round(request_time, 2)}s-{request.method}-{request.url.path.replace("/", "_")}-{uuid4()}.{extension}"
                # If time limit is specified, only profiles that are over the given limit are stored.
                time_limit: float = request.query_params.get("profile_time_limit", 0.0)
                should_store_profile: bool = request_time > float(time_limit)
                if should_store_profile:
                    if config.PROFILING_STORAGE_ACCOUNT:
                        # Store profiles in Azure blob storage
                        def send_profile_request_to_azure(data):
                            blob_service = BlobServiceClient.from_connection_string(config.PROFILING_STORAGE_ACCOUNT)
                            container_client = blob_service.get_container_client(container="profiles")
                            container_client.upload_blob(name=file_name, data=data)
                            logger.info(f"A request profile is uploaded to Azure blob storage: {file_name}")

                        background_tasks = BackgroundTasks()
                        background_tasks.add_task(
                            send_profile_request_to_azure, data=profiler.output(renderer=renderer)
                        )
                        response.background = background_tasks
                    else:
                        # Store profiles on disk
                        with open(Path(__file__).parent / f"profiles/{file_name}", "w") as out:
                            out.write(profiler.output(renderer=renderer))
                        logger.info(f"A request profile is stored on disk: {file_name}")
                return response
            return await call_next(request)

    @app.get(
        "/",
        operation_id="redirect_to_docs",
        response_class=RedirectResponse,
        include_in_schema=False,
    )
    def redirect_to_docs():
        """
        Redirects any requests to the servers root ('/') to '/docs'
        """
        return RedirectResponse(url="/docs")

    return app


@click.group()
def cli():
    pass


@cli.command()
def run():
    uvicorn.run(
        "app:create_app",
        host="0.0.0.0",  # noqa: S104
        port=5000,
        access_log=False,
        reload=config.ENVIRONMENT == "local",
        log_level=config.LOGGER_LEVEL.lower(),
    )


@cli.command()
def init_application():
    logger.info("IMPORTING CORE DOCUMENTS")
    # Running commands locally sets the user_context to "DMSS_ADMIN"
    user = User(
        **{
            "user_id": config.DMSS_ADMIN,
            "full_name": "Local Admin",
            "email": "admin@example.com",
        }
    )
    import_package(
        "/code/src/SIMOS",
        user,
        data_source_name=config.CORE_DATA_SOURCE,
        is_root=True,
    )
    create_lookup_table_use_case(["system/SIMOS/recipe_links"], "DMSS", user)


@cli.command()
@click.argument("file")
def import_data_source(file):
    with open(file) as json_file:
        document = json.load(json_file)
        # Running commands locally sets the user_context to "DMSS_ADMIN"
        user = User(
            **{
                "user_id": config.DMSS_ADMIN,
                "full_name": "Local Admin",
                "email": "admin@example.com",
            }
        )
        DataSourceRepository(user).create(document["name"], DataSourceRequest(**document))


@cli.command()
def nuke_db():
    logger.info("EMPTYING DATABASES")
    databases = mongo_client.list_database_names()
    # Don't touch the mongo admin or local database
    databases = [databasename for databasename in databases if databasename not in ("admin", "local", "config")]
    logger.warning(f"Emptying databases {databases}")
    for db_name in databases:
        print(db_name)
        logger.debug(f"Deleting all documents from database '{db_name}' from the DMSS system MongoDB server")
        for collection in mongo_client[db_name].list_collection_names():
            mongo_client[db_name][collection].delete_many({})
        blob_handler = gridfs.GridFS(mongo_client[db_name])
        for filename in blob_handler.list():
            blob_handler.delete(filename)
    logger.debug("DONE")


@cli.command()
@click.pass_context
def reset_app(context):
    context.invoke(nuke_db)
    logger.info("CREATING SYSTEM DATA SOURCE")
    context.invoke(import_data_source, file="/tmp/DMSS_systemDS.json")  # noqa: S108
    logger.debug("DONE")
    context.invoke(init_application)


@cli.command()
@click.pass_context
def create_key(context):
    key = context.invoke(generate_key)
    print(key)


if __name__ == "__main__":
    cli()
