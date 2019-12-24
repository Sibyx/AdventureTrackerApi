from api.errors import ApiException, ValidationException
from api.response import ErrorResponse, ValidationResponse


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ApiException):
            return ErrorResponse.create_from_exception(exception)
        elif isinstance(exception, ValidationException):
            return ValidationResponse.create_from_exception(exception)
