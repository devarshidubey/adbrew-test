from rest_framework.exceptions import APIException

class HTTPError(APIException):
    status_code = 500
    default_detail = "A server error occurred."
    default_code = "error"

    def __init__(self, status_code, message):
        super().__init__(detail=message)
        self.message = message
        self.status_code = status_code
