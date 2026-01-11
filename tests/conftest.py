import os

import pytest
from typing import Generator
from src.base_client import BaseClient


@pytest.fixture(scope="session")
def client() -> Generator[BaseClient, None, None]:
    """
    Fixture that initializes the BaseClient.
    """
    api_client = BaseClient()
    yield api_client


@pytest.fixture(scope="session", autouse=True)
def authenticate(client: BaseClient):
    """
    Performs login and injects the token into the existing client.
    """

    username = os.getenv("API_PASSWORD")
    password = os.getenv("API_PASSWORD")

    if not username or not password:
        raise EnvironmentError("Please set API_PASSWORD and API_PASSWORD environment variables")

    payload = {
        "username": username,
        "password": password,
    }

    response = client.post("/auth", payload)
    assert response.status_code == 200, "Authentication failed"

    # המרת התשובה
    auth_data = response.json()

    # בדיקת טיפוס (כמו שביקשת להשאיר)
    assert isinstance(auth_data, dict), "Response format invalid: expected a dictionary"

    # חילוץ הטוקן והזרקה ל-Headers
    token = auth_data.get("token")
    client.headers.update({"Cookie": f"token={token}"})