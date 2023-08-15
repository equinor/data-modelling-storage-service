from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from features.meta.use_cases.get_meta_use_case import get_meta_use_case

router = APIRouter(tags=["default", "meta"], prefix="/meta")


@router.get(
    "/{data_source_id}/{document_id}",
    operation_id="meta_by_id",
    responses={
        **responses,
    },
    response_model=dict,
)
@create_response(JSONResponse)
def get_meta_by_id(data_source_id: str, document_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Get Meta Information About a Document. 
    
    This endpoint returns meta information about a document provided document id and the id of the data source of which it is located.

    Args: 
        data_source_id (str): The ID of the data source.
        document_id (str): The ID of the document. 

    Returns: 
        dict: A dictionary containing the meta infomation about the document
            Example: 
            {
                "type": "CORE:Meta",
                "version": "0.0.1",
                "dependencies": [
                    {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "CORE",
                    "address": "system/SIMOS",
                    "version": "0.0.1",
                    "protocol": "dmss"
                    }
                ]
            }
    """
    return get_meta_use_case(user=user, data_source_id=data_source_id, document_id=document_id)
