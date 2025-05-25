from typing import Any, Dict, List, Optional, Union

from beanie import Document, PydanticObjectId
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


def build_json_response(
    status_code: int,
    context: str,
    element: Optional[Union[List[dict], dict]],
) -> JSONResponse:

    if element is None:
        content = {
            "status": True,
            "status_code": status_code,
            "message": context,
        }
    else:

        content = {
            "status": True,
            "status_code": status_code,
            "message": context,
            "data": element if not isinstance(element, Dict) else dict_to_json(element),
        }

    return JSONResponse(status_code=status_code, content=content)


def dict_to_json(dict: Optional[Union[List[dict], dict]]):
    result = []
    if not isinstance(dict, List):
        return [
            jsonable_encoder(
                {
                    k: str(v) if isinstance(v, (PydanticObjectId, ObjectId)) else v
                    for k, v in dict.items()
                }
            )
        ]
    else:
        for v in dict:
            json_type = jsonable_encoder(
                {
                    k: str(v) if isinstance(v, (PydanticObjectId, ObjectId)) else v
                    for k, v in v.items()
                }
            )
            result.append(json_type)
        return json_type


def serializable_format(element: any) -> dict:
    element.id = str(element.id)
    element.file_infos = str(element.file_infos)
    element.docker_infos = str(element.docker_infos)
    dict_type = element.model_dump()
    return {
        k: str(v) if isinstance(v, (PydanticObjectId, ObjectId)) else v
        for k, v in dict_type.items()
    }


def beanie_document_to_dict(
    document: Union[Document, BaseModel, Dict, List, Any],
) -> Union[Dict, List, Any]:
    # Handle None values
    if document is None:
        return None

    # Handle ObjectId and PydanticObjectId directly
    if isinstance(document, (ObjectId, PydanticObjectId)):
        return str(document)

    # Handle Beanie Document or Pydantic BaseModel
    if isinstance(document, (Document, BaseModel)):
        # Use model_dump() for Pydantic v2 or dict() for v1
        try:
            doc_dict = document.model_dump()
        except AttributeError:
            doc_dict = document.dict()

        return _process_dict(doc_dict)

    # Handle regular dictionaries
    elif isinstance(document, dict):
        return _process_dict(document)

    # Handle lists
    elif isinstance(document, list):
        return [beanie_document_to_dict(item) for item in document]

    # Handle other types (str, int, float, bool, etc.)
    else:
        return document


def _process_dict(doc_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a dictionary, converting ObjectIds to strings recursively.

    Args:
        doc_dict: Dictionary to process

    Returns:
        Processed dictionary with ObjectIds as strings
    """
    result = {}

    for key, value in doc_dict.items():
        # Convert ObjectId and PydanticObjectId to string
        if isinstance(value, (ObjectId, PydanticObjectId)):
            result[key] = str(value)

        # Recursively handle nested dictionaries
        elif isinstance(value, dict):
            result[key] = _process_dict(value)

        # Recursively handle lists
        elif isinstance(value, list):
            result[key] = [beanie_document_to_dict(item) for item in value]

        # Handle nested Beanie documents or Pydantic models
        elif isinstance(value, (Document, BaseModel)):
            result[key] = beanie_document_to_dict(value)

        # Keep other types as they are
        else:
            result[key] = value

    return result
