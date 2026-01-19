import logging
import os
from typing import Generator

import pytest
from dotenv import load_dotenv

from src.clients.base_client import BaseClient
from src.models.auth.auth_models import AuthRequst, AuthResponse

@pytest.fixture(scope="session", autouse=True)
def loading_environments_variables() -> None:
    """
    Fixture that initializes the environments variables
    """
    if not load_dotenv(".env"):
        raise FileNotFoundError(".env file missing! Please check your .env file")

    _REQUIRED_ENV = [
        "BASE_URL",
        "ADMIN_USERNAME",
        "ADMIN_PASSWORD",
    ]

    missing_env: [str] = []
    for env in _REQUIRED_ENV:
        if env not in os.environ:
            missing_env.append(env)

    if missing_env:
        raise EnvironmentError(f"CRITICAL: Missing environments_variables: {', '.join(missing_env)}")
        
    logging.info("Initialized Loading Environments Variables fixture")


@pytest.fixture(scope="session")
def client(loading_environments_variables: None) -> Generator[BaseClient, None, None]:
    """
    Fixture that initializes once the BaseClient.
    """
    api_client = BaseClient()
    logging.info("Initialized BaseClient fixture")
    yield api_client


@pytest.fixture(scope="session", autouse=True)
def authenticate(client: BaseClient):
    """
    Performs login once and injects the token into the existing BaseClient.
    """

    auth_requst = AuthRequst(
        username=os.environ["ADMIN_USERNAME"],
        password=os.environ["ADMIN_PASSWORD"]
    )

    response = client.post("/auth", auth_requst.model_dump())
    assert response.status_code == 200, "Authentication failed"

    auth_response: AuthResponse = AuthResponse(**response.json())

    client.headers.update({"Authorization": auth_response.token})
    logging.info("Authentication successful. Token Passed to Request Headers")
    