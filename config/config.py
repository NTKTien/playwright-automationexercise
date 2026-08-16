import os

ENV = os.getenv("TEST_ENV", "prod").lower()

ENV_URLS = {
    "local": "",
    "staging": "",
    "prod": "https://automationexercise.com"
}

BASE_URL = ENV_URLS.get(ENV, ENV_URLS["prod"])
DEFAULT_TIMEOUT = 30000
TIMEOUT_FAST_FAIL = 1500
TIMEOUT_STANDARD = 5000
TIMEOUT_ELEMENT_CHECK = 3000
WAIT_NO_RESULT = 1000  
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "test_data.xlsx")
SLOW_MO = int(os.getenv("SLOW_MO", "0"))