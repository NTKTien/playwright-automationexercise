import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from utils.excel_utils import load_excel_data
from config.config import DATA_FILE
from utils.logger import get_logger

logger = get_logger(__name__)
login_cases = load_excel_data(DATA_FILE, "LoginData")

@pytest.mark.parametrize("case", login_cases)
def test_login_flow(driver_setup, request, case):
    request.node.test_id = case.get("TestCaseID", "LoginTest")
    logger.info(f"--- Starting test: {request.node.test_id} ---")
    
    page = driver_setup["page"]
    login_page = LoginPage(page)
    expected_result = str(case.get("ExpectedResult")).strip().upper()
    
    # 1. Initialize access
    login_page.navigate("/login")
    email = case.get("Email Address")
    password = case.get("Password")
    
    # 2. Perform Login
    login_page.perform_login(email, password)
    
    # 3. Analyze results
    system_error = login_page.get_login_error()
    html5_error = login_page.get_html5_validation_error()
    
    if system_error or html5_error:
        error_msg = system_error or html5_error
        logger.info(f"Found login error: '{error_msg}'")
        if expected_result == "FAIL":
            assert True, f"Pass expected FAIL with error: {error_msg}"
        else:
            pytest.fail(f"Expected SUCCESS but encountered error: '{error_msg}'")
            
    else:
        if expected_result == "SUCCESS":
            try:
                login_page.verify_login_success()
                logger.info("Login successful, found 'Logged in as' message in the header.")
            except AssertionError as e:
                pytest.fail(f"Success message not found: {str(e)}")
        else:
            try:
                # If expecting FAIL but login is successful
                login_page.verify_login_success()
                pytest.fail("Expected FAIL but the account logged in successfully.")
            except AssertionError:
                logger.info("Failed to login as expected (FAIL).")