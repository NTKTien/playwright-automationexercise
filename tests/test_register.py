import pytest
from playwright.sync_api import expect
from pages.register_page import RegisterPage
from locators.register_locators import RegisterLocators
from utils.excel_utils import load_excel_data
from config.config import DATA_FILE
from utils.logger import get_logger
from config.config import TIMEOUT_ELEMENT_CHECK

logger = get_logger(__name__)
register_cases = load_excel_data(DATA_FILE, "RegisterData")

@pytest.mark.parametrize("case", register_cases)
def test_register_flow(driver_setup, request, case):
    request.node.test_id = case.get("TestCaseID", "RegisterTest")
    logger.info(f"--- Bắt đầu test: {request.node.test_id} ---")
    
    page = driver_setup["page"]
    register_page = RegisterPage(page)
    expected_result = str(case.get("ExpectedResult")).strip().upper()
    
    # =======================================================
    # STEP 1: PROCESS INITIAL LOGIN/SIGNUP FORM
    # =======================================================
    register_page.navigate("/login")
    register_page.fill_initial_signup(case.get("SignupName"), case.get("SignupEmailAddress"))
    
    system_error = register_page.get_system_error()
    html5_error = register_page.get_html5_validation_error()
    
    if system_error or html5_error:
        error_msg = system_error or html5_error
        logger.info(f"Found error in step 1: '{error_msg}'")
        if expected_result == "FAIL":
            assert True, f"Pass expected FAIL with error: {error_msg}"
            return
        else:
            pytest.fail(f"Expected SUCCESS but encountered error: '{error_msg}'")

    # =======================================================
    # STEP 2: FILL IN ACCOUNT DETAILS
    # =======================================================
    try:
        register_page.fill_account_details(case)
    except Exception as e:
        if expected_result == "FAIL":
            logger.info("Failed to fill the form (Pass expected FAIL).")
            return
        else:
            pytest.fail(f"Error occurred while filling Account Details: {str(e)}")

    form_error = register_page.get_html5_validation_error()
    if form_error:
        logger.info(f"Found validation error in form: '{form_error}'")
        if expected_result == "FAIL":
            assert True
            return
        else:
            pytest.fail(f"Expected SUCCESS but form reported error: '{form_error}'")

    # =======================================================
    # STEP 3: CONFIRM RESULT & ALWAYS CLEAN UP (TEARDOWN)
    # =======================================================
    is_created = page.locator(RegisterLocators.ACCOUNT_CREATED_MSG).is_visible(timeout=TIMEOUT_ELEMENT_CHECK)

    if is_created:
        # Press Continue to go to the home page
        register_page.click(RegisterLocators.CONTINUE_BTN)
        expected_name = case.get("AccountName") or case.get("SignupName")
        
        # If test case belongs to the SUCCESS flow, proceed to verify Header
        verify_error = None
        if expected_result == "SUCCESS":
            try:
                register_page.verify_logged_in_as(expected_name)
            except Exception as e:
                verify_error = e
                
        # CLEAN UP ACCOUNT
        try:
            register_page.delete_account()
            logger.info(f"Automatically cleaned up: Account '{expected_name}' deleted successfully.")
        except Exception as e:
            logger.error(f"Failed to delete account for cleanup: {e}")
            
        # Assertion about the Test Case after cleanup
        if expected_result == "FAIL":
            pytest.fail("System Bug: Expected FAIL but the account was created successfully (Account automatically deleted).")
        elif verify_error:
            pytest.fail(f"Account created successfully but error occurred while displaying Header: {verify_error}")
        else:
            logger.info("Registration successful and full name displayed in the header.")

    else:
        # Account not created
        if expected_result == "SUCCESS":
            pytest.fail("Expected SUCCESS but the account was not created.")
        else:
            logger.info("Pass: Systems blocks account creation as expected (FAIL).")