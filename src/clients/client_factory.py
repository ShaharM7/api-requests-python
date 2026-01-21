import os
from src.clients.abstract_base_client import AbstractBaseClient
from src.clients.requests_client import RequestsClient

class ClientFactory:
    """Factory to create the right HTTP client accourding env variable"""

    # @staticmethod 
    ## There is no requirement that the factory creation method to be static
    def create_client() -> AbstractBaseClient:
        client_type = os.getenv("HTTP_CLIENT", "requests").lower()
        
        if client_type == "requests" :
            return RequestsClient()
        elif client_type == "azure": 
            raise NotImplementedError("AzureDevOpsClient Not Implemented Yet")
        elif client_type == "awd":
            raise NotImplementedError("AWSClient Not Implemented Yet")
        else:
            raise ValueError(f"Unkown client type: {client_type}")
