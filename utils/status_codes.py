import enum


class StatusCode(enum.Enum):
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    ERROR = 500
