from app.packages.constant.http_exception_errors import Http_execption_code
from app.packages.helpers.build_functions_responses import build_json_response


class ExceptionCase(Exception):
    def __init__(self, context: str):
        self.exception_case = self.__class__.__name__
        self.context = context

    def json(self):
        return build_json_response(
            Http_execption_code[self.exception_case], self.context
        )


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
