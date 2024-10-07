import os
from dotenv import load_dotenv

load_dotenv()

AGENTQL_API_KEY = os.getenv("AGENTQL_API_KEY")

def get_agentql_api_key() -> str:
    return AGENTQL_API_KEY

def handle_rate_limiting(response: dict) -> None:
    # Implement rate limiting logic here
    pass