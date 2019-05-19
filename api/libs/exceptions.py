from api.configs.utils import HTTPStatusCodes


class FailedRequestException(Exception):
    def __init__(self, message, status_code=HTTPStatusCodes.INTERNAL_SERVER_ERROR):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def get_message(self):
        return self.message

    def get_status_code(self):
        return self.status_code


class InvalidOperatorException(Exception):
    pass
