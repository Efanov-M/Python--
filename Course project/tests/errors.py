class YaDiskAPIError(Exception):
    def __init__(self, status_code, message=None):
        self.status_code = status_code
        self.message = message or "API error"
        super().__init__(f"{self.message} (HTTP {self.status_code})")


class CatApiError(Exception):
    def __init__(self, status_code, message=None):
        self.status_code = status_code
        self.message = message or "API error"
        super().__init__(f"{self.message} (HTTP {self.status_code})")
