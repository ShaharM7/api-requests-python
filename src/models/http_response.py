class HttpResponse:
    """
    Generic HTTP response wrapper.
    Works with ANY HTTP client - Requests, Azure, AWS, etc.
    """

    def __init__(self, status_code: int, body: str, headers: dict = None) -> None:
        self._status_code = status_code
        self._body = body
        self._headers = headers or {}

    @property
    def status_code(self):
        """HTTP status code (200, 404, etc.)"""
        return self._status_code
    
    @property
    def text(self) -> str:
        """Response body as text"""
        return self._body

    def json(self) -> dict | list:
        """Response body as Python object"""
        import json
        return json.loads(self._body)

    @property
    def headers(self) -> dict | None:
        """Response headers"""
        return self._headers

    def raise_for_status(self) -> None:
        """
        Raise an exception if status code indicates an error (4xx or 5xx).
        If successful (2xx), does nothing.
        """
        if 400 <= self._status_code < 600:
            from requests.exceptions import HTTPError
            raise HTTPError(
                f"{self._status_code} Client Error: {self._body[:200]}",
                response=self
            )