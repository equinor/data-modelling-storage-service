from typing import List, Optional

from pydantic import BaseModel
from requests import HTTPError, Request, Session, post

from common.utils.logging import logger
from config import config

GRAPH_API_URL = "https://graph.microsoft.com/v1.0"


class GraphRequest(BaseModel):
    path: str
    method: str = "GET"
    data: Optional[dict] = {}
    params: Optional[dict] = {}
    headers: Optional[dict] = {}
    payload: Optional[dict] = {}


class CredentialRequest(BaseModel):
    client_id: str
    client_secret: str


class AppRole(BaseModel):
    id: str
    displayName: str
    value: str
    isEnabled: bool


class AppRolesResponse(BaseModel):
    value: List[AppRole]


class AppRoleAssignment(BaseModel):
    id: str
    appRoleId: str
    principalId: str
    principalDisplayName: str


class AppRolesAssignedResponse(BaseModel):
    value: List[AppRoleAssignment]


def get_graph_api_access_token(credentials: CredentialRequest):
    url = config.OAUTH_TOKEN_ENDPOINT
    grant_type = "client_credentials"

    payload = (
        f"client_id={credentials.client_id}&"
        f"grant_type={grant_type}&"
        f"client_secret={credentials.client_secret}&"
        f"scope=https%3A%2F%2Fgraph.microsoft.com%2F.default"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        res = post(url, headers=headers, data=payload)
        res.raise_for_status()
        auth_response = res.json()
        return auth_response["access_token"]
    except HTTPError as http_err:
        logger.error(http_err)
        if http_err.response:
            logger.error(http_err.response.json())
        raise


def graph_request(request: GraphRequest):
    """
    Query the Microsoft Graph API
    """
    session = Session()
    try:
        url = f"{GRAPH_API_URL}/{request.path}"
        headers = request.headers
        access_token = get_graph_api_access_token(
            CredentialRequest(client_id=config.OAUTH_CLIENT_ID, client_secret=config.OAUTH_CLIENT_SECRET)
        )
        headers["Authorization"] = f"Bearer {access_token}"

        _req = Request(
            url=url,
            method=request.method,
            data=request.data,
            headers=headers,
            params=request.params,
            json=request.payload,
        )
        req = _req.prepare()
        response = session.send(req)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        logger.error(http_err)
        if http_err.response:
            logger.error(http_err.response.json())
        raise


def get_app_roles() -> List[AppRole]:
    """
    https://docs.microsoft.com/en-us/graph/api/resources/approle
    The roles exposed by the application which this service principal represents.
    """
    path = f"servicePrincipals/{config.AAD_ENTERPRISE_APP_OID}/appRoles"
    response = graph_request(GraphRequest(path=path))
    app_roles_response = AppRolesResponse(**response)

    return app_roles_response.value


def get_app_roles_assigned_to() -> List[AppRoleAssignment]:
    """
    https://docs.microsoft.com/en-us/graph/api/serviceprincipal-list-approleassignedto
    Retrieve a list of appRoleAssignment that users, groups, or client service principals
    have been granted for the given resource service principal.
    """
    path = f"servicePrincipals/{config.AAD_ENTERPRISE_APP_OID}/appRoleAssignedTo"
    response = graph_request(GraphRequest(path=path))
    app_roles_assigned_response = AppRolesAssignedResponse(**response)

    return app_roles_assigned_response.value
