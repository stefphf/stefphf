from __future__ import annotations


class APIError(Exception):
    message: str
    status_code: int

    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code

    @classmethod
    def bad_request(cls, message: str) -> APIError:
        return cls(message, status_code=400)

    @classmethod
    def permission_denied(cls, message: str) -> APIError:
        return cls(message, status_code=403)

    @classmethod
    def internal(cls, message: str) -> APIError:
        return cls(message, status_code=500)
