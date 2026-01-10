import os
from dotenv import load_dotenv

load_dotenv("../.env")

class Config:

    BASE_URL = os.getenv("BASE_URL")

    if not BASE_URL:
        raise ValueError(f"BASE_URL is missing! Please check your configuration")