from abc import ABC, abstractmethod
from src.models.http_response import HttpResponse

class AbstractBaseClient(ABC):
    """Abstract interface for all HTTP/S clients"""

    @abstractmethod
    def get(self, endpoint: str, params: dict = None, **kwargs) -> HttpResponse:
        pass
        
    @abstractmethod
    def post(self, endpoint: str, payload: dict, **kwargs) -> HttpResponse:
        pass
    
    @abstractmethod
    def put(self, endpoint: str, payload: dict, **kwargs) -> HttpResponse:
        pass

    @abstractmethod
    def patch(self, endpoint: str, payload: dict, **kwargs) -> HttpResponse:
        pass

    @abstractmethod
    def delete(self, endpoint: str, **kwargs) -> HttpResponse:
        pass

    @abstractmethod
    def update_headers(self, headers: dict) -> None:
        pass
