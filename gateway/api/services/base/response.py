from dataclasses import dataclass


@dataclass
class Response:
    """Base API response"""

    status: str
    message: str

    def dict(self) -> dict:
        return {'status': self.status, 'message': self.message}


class ErrorResponse(Response):
    """Error API response"""

    def __init__(self, message: str = ''):
        super().__init__('error', message)


class SuccessResponse(Response):
    """Successful API response"""

    data: list

    def __init__(self, data: list, message: str = ''):
        super().__init__('success', message)
        self.data = data

    def dict(self) -> dict:
        res = super().dict()
        res['data'] = self.data
        if not self.message:
            res.pop('message')
        return res
