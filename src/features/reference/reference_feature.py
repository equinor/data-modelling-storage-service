from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.delete_reference_use_case import delete_reference_use_case

router = APIRouter(tags=["default", "reference"], prefix="/reference")


@router.delete("/{address:path}", operation_id="reference_delete", response_model=dict, responses=responses)
@create_response(JSONResponse)
def delete_reference(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Delete a reference in an entity.

    Used to delete uncontained attributes in an entity.

    - **document_dotted_id**: <data_source>/<path_to_entity>/<entity_name>.<attribute>
    """
    return delete_reference_use_case(user=user, address=address)
