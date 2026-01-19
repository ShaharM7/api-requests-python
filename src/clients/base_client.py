import os
import requests
from requests import Response


class BaseClient:
    """
    A wrapper class for the requests' library.
    All API interactions should go through this class to ensure consistency.
    """

    def __init__(self):
        self.base_url = os.environ["BASE_URL"]
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get(self, endpoint: str, params: dict = None, **kwargs) -> Response:
        """
        Sends a GET request.
        :param endpoint: API endpoint (e.g., '/booking')
        :param params: (Optional) Dictionary of query parameters
        :param kwargs: (Optional) Extra arguments for requests (timeout, auth, etc.)
        :return: Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params, **kwargs)
        return response

    def post(self, endpoint: str, payload: dict, **kwargs) -> Response:
        """
        Sends a POST request.
        :param endpoint: API endpoint
        :param payload: Request body (Dictionary)
        :param kwargs: (Optional) Extra arguments for requests
        :return: Response object
        """
        url = f"{self.base_url}{endpoint}"
        # 'json=' automatically serializes the dictionary to a JSON string
        response = requests.post(url, headers=self.headers, json=payload, **kwargs)
        return response

    def put(self, endpoint: str, payload: dict, **kwargs) -> Response:
        """
        Sends a PUT request.
        :param endpoint: API endpoint
        :param payload: Request body to update
        :param kwargs: (Optional) Extra arguments for requests
        :return: Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, headers=self.headers, json=payload, **kwargs)
        return response

    def delete(self, endpoint: str, **kwargs) -> Response:
        """
        Sends a DELETE request.
        :param endpoint: API endpoint
        :param kwargs: (Optional) Extra arguments for requests
        :return: Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self.headers, **kwargs)
        return response
