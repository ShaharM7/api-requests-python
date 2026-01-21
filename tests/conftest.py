import logging
import os

import pytest
from dotenv import load_dotenv

from src.clients.facades.auth_client import AuthClient
from src.clients.abstract_base_client import AbstractBaseClient
from src.clients.facades.booking_client import BookingClient
from src.clients.client_factory import ClientFactory
from src.models.auth.auth_models import AuthResponse


@pytest.fixture(scope="session", autouse=True)
def loading_environments_variables():
    """
    Fixture that initializes the environments variables
    """
    if not load_dotenv(".env"):
        raise FileNotFoundError(".env file missing! Please check your .env file")

    _REQUIRED_ENV: [] = [
        "BASE_URL",
        "HTTP_CLIENT",
        "ADMIN_USERNAME",
        "ADMIN_PASSWORD",
    ]

    _missing_env: [str] = []
    for env in _REQUIRED_ENV:
        if env not in os.environ:
            _missing_env.append(env)

    if _missing_env:
        raise EnvironmentError(f"CRITICAL: Missing environments_variables: {', '.join(_missing_env)}")
        
    logging.info("Finish Loading Environments Variables")


@pytest.fixture(scope="session")
def factory_creation_client(loading_environments_variables) -> AbstractBaseClient:
    """
    Fixture that using factory pattern to create rest api client depened on env varaible
    """
    client: AbstractBaseClient = ClientFactory.create_client()
    logging.info(f"Factory Creation {os.getenv("HTTP_CLIENT")} Client")
    return client


# Clients - simillar to steps
@pytest.fixture(scope="session")
def initialize_auth_client(factory_creation_client) -> AuthClient:
    auth_client: AuthClient = AuthClient(factory_creation_client)
    logging.info("Initialized Auth Client")
    return auth_client


@pytest.fixture(scope="session", autouse=True)
def authenticate_and_pass_token_to_header(factory_creation_client: AbstractBaseClient, initialize_auth_client: AuthClient):
    """
    Performs login once and injects the token into the existing AbstractBaseClient.
    """
    auth_response: AuthResponse = initialize_auth_client.authenticate()
    factory_creation_client.update_headers({"Authorization": auth_response.token})
    logging.info("Authentication successful. Token Passed to Request Header")


@pytest.fixture(scope="session")
def initialize_booking_client(authenticate_and_pass_token_to_header) -> BookingClient:
    booking_client: BookingClient = BookingClient(factory_creation_client)
    logging.info("Initialized Booking Client")
    return booking_client
    