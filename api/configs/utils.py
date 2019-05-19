import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
LOGS_FOLDER = os.path.join(PROJECT_ROOT, "logs")
if not os.path.exists(LOGS_FOLDER):
    os.mkdir(LOGS_FOLDER)



class HTTPStatusCodes(object):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409

    INTERNAL_SERVER_ERROR = 500
