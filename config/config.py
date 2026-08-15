import os

ENV = os.getenv("TEST_ENV", "prod").lower()

ENV_URLS = {
    "local": "http://localhost:3000",
    "staging": "https://staging.automationexercise.com",
    "prod": "https://automationexercise.com"
}

BASE_URL = ENV_URLS.get(ENV, ENV_URLS["prod"])
DEFAULT_TIMEOUT = 30000
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "test_data.xlsx")
SLOW_MO = int(os.getenv("SLOW_MO", "0"))