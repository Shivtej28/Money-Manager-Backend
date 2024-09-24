class Response:
    def __init__(
        self,
        is_success=False,
        status_code= int(),
        result=None,
        message=str(),
    ):
     self.is_success = is_success
     self.status_code = status_code
     self.result = result
     self.message = message

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "is_success": self.is_success,
            "message": self.message,
            "result": self.result
        }
        