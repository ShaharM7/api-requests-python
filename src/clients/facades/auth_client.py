import os

from dotenv.main import logger
from pydantic import BaseModel
from src.clients.abstract_base_client import AbstractBaseClient
from src.models.auth.auth_models import AuthRequest, AuthResponse
from src.models.http_response import HttpResponse


class AuthClient:
    """
    High-level auth API (Facade Pattern).
    Hides HTTP complexity from tests.
    """ 

    def __init__(self, client: AbstractBaseClient) -> None:
        self.client = client
        self.auth_endpoint = "/auth"

    def authenticate(self) -> AuthResponse:
        auth_model_request: BaseModel = AuthRequest(
            username=os.getenv("ADMIN_USERNAME"),
            password=os.getenv("ADMIN_PASSWORD")
         )

        http_response: HttpResponse = self.client.post(endpoint=self.auth_endpoint, payload=auth_model_request.model_dump(mode="json"))
        assert http_response.status_code == 200, f"Authentication Failed"

        return AuthResponse(**http_response.json())



