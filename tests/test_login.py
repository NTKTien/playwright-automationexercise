import pytest
from pages.login_page import LoginPage
from utils.excel_utils import load_excel_data
from config.config import DATA_FILE
from utils.logger import get_logger

logger = get_logger(__name__)
login_cases = load_excel_data(DATA_FILE, "LoginData")

@pytest.mark.parametrize("case", login_cases)
def test_login(driver_setup, request, case):
    request.node.test_id = case.get("TestCaseID", "LoginTest")
    logger.info(f"Running Test: {request.node.test_id} on {driver_setup['browser_name']}")
    
    page = driver_setup["page"]
    login_page = LoginPage(page)
    
    login_page.navigate("/login")
    login_page.perform_login(case.get("User"), case.get("Password"))

    if str(case.get("ExpectedResult")).upper() == "SUCCESS":
        login_page.verify_login_success()
    else:
        login_page.verify_login_failed(case.get("ErrorMessage", "incorrect"))