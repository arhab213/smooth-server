from enum import IntEnum


class Http_execption_code(IntEnum):
    BadRequest = 400
    NotFound = 404
    InternalServer = 500
    Forbidden = 403
    Unauthorized = 401
    StatusOK = 200
    Created = 201
