from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from common.responses import create_response

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from restful.request_types.shared import Reference
from .use_cases.delete_reference_use_case import delete_reference_use_case
from .use_cases.insert_reference_use_case import insert_reference_use_case

router = APIRouter(tags=["default", "reference"], prefix="/reference")


@router.put("/{data_source_id}/{document_dotted_id}", operation_id="reference_insert", response_model=dict)
@create_response(JSONResponse)
def insert_reference(
    data_source_id: str, document_dotted_id: str, reference: Reference, user: User = Depends(auth_w_jwt_or_pat)
):
    document_id, attribute = document_dotted_id.split(".", 1)
    return insert_reference_use_case(
        user=user, data_source_id=data_source_id, document_id=document_id, reference=reference, attribute=attribute
    )


@router.delete("/{data_source_id}/{document_dotted_id}", operation_id="reference_delete", response_model=dict)
@create_response(JSONResponse)
def delete_reference(data_source_id: str, document_dotted_id: str, user: User = Depends(auth_w_jwt_or_pat)):

    document_id, attribute = document_dotted_id.split(".", 1)
    return delete_reference_use_case(
        user=user, document_id=document_id, data_source_id=data_source_id, attribute=attribute
    )
