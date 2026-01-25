import os
from requests import Response
import requests

from src.clients.abstract_base_client import AbstractBaseClient
from src.models.http_response import HttpResponse

class RequestsClient(AbstractBaseClient):
    """Requests library implementation of AbstractBaseClient"""

    def __init__(self) -> None:
        self.base_url = os.environ["BASE_URL"]
        self.headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get(self, endpoint: str, params: dict = None, **kwargs) -> HttpResponse:
        url=f"{self.base_url}{endpoint}"
        return self._convert_requests_response_to_http_response(
            requests.get(url=url, headers=self.headers, params=params, **kwargs)
        )
    
    def post(self, endpoint: str, payload: dict = None, **kwargs) -> HttpResponse:
        url=f"{self.base_url}{endpoint}"
        return self._convert_requests_response_to_http_response(
            requests.post(url=url, headers=self.headers, json=payload, **kwargs)
        )

    def put(self, endpoint: str, payload: dict = None, **kwargs) -> HttpResponse:
        url=f"{self.base_url}{endpoint}"
        return self._convert_requests_response_to_http_response(
            requests.put(url=url, headers=self.headers, json=payload, **kwargs)
        )

    def patch(self, endpoint: str, payload: dict = None, **kwargs) -> HttpResponse:
        url=f"{self.base_url}{endpoint}"
        return self._convert_requests_response_to_http_response(
            requests.patch(url=url, headers=self.headers, json=payload, **kwargs)
        )

    def delete(self, endpoint: str, **kwargs) -> HttpResponse:
        url=f"{self.base_url}{endpoint}"
        return self._convert_requests_response_to_http_response(
            requests.delete(url=url, headers=self.headers, **kwargs)
        )

    def update_headers(self, headers: dict) -> None:
        self.headers.update(headers)

    def _convert_requests_response_to_http_response(self, resposne: Response) -> HttpResponse:
        return HttpResponse(
            status_code=resposne.status_code,
            body=resposne.text,
            headers=dict(resposne.headers)
            )
