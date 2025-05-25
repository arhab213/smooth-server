from typing import List, Optional, Union

from app.packages.constant.http_exception_errors import Http_execption_code
from app.packages.helpers.build_functions_responses import build_json_response


class ExceptionCase(Exception):
    def __init__(self, context: str, element: Optional[Union[List[dict], dict]]):
        self.exception_case = self.__class__.__name__
        self.context = context
        self.status_code = Http_execption_code[str(self.exception_case)].value
        self.element = element

    def json(self):
        return build_json_response(self.status_code, self.context, self.element)

    def dict(self):
        return {
            "status": True,
            "status_code": self.status_code,
            "message": self.context,
        }


class AppException:

    class BadRequest(ExceptionCase):
        pass

    class NotFound(ExceptionCase):
        pass

    class InternalServer(ExceptionCase):
        pass

    class Forbidden(ExceptionCase):
        pass

    class Unauthorized(ExceptionCase):
        pass

    class StatusOK(ExceptionCase):
        pass

    class Created(ExceptionCase):
        pass
