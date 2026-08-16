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
    logger.info(f"--- Bắt đầu test: {request.node.test_id} ---")
    
    page = driver_setup["page"]
    login_page = LoginPage(page)
    expected_result = str(case.get("ExpectedResult")).strip().upper()
    
    # 1. Khởi tạo truy cập
    login_page.navigate("/login")
    
    # Lấy đúng tên cột trong Excel theo ảnh của bạn: "Email Address" và "Password"
    email = case.get("Email Address")
    password = case.get("Password")
    
    # 2. Thực hiện Đăng nhập
    login_page.perform_login(email, password)
    
    # 3. Phân tích kết quả
    system_error = login_page.get_login_error()
    html5_error = login_page.get_html5_validation_error()
    
    if system_error or html5_error:
        error_msg = system_error or html5_error
        logger.info(f"Bắt được lỗi login: '{error_msg}'")
        if expected_result == "FAIL":
            assert True, f"Pass đúng kỳ vọng FAIL với lỗi: {error_msg}"
        else:
            pytest.fail(f"Kỳ vọng SUCCESS nhưng gặp lỗi: '{error_msg}'")
            
    else:
        if expected_result == "SUCCESS":
            try:
                login_page.verify_login_success()
                logger.info("Đăng nhập thành công, đã tìm thấy Logged in as trên header.")
            except AssertionError as e:
                pytest.fail(f"Không thấy thông báo thành công: {str(e)}")
        else:
            try:
                # Nếu kỳ vọng Fail nhưng lại login được
                login_page.verify_login_success()
                pytest.fail("Kỳ vọng FAIL nhưng tài khoản lại login thành công.")
            except AssertionError:
                logger.info("Không login được đúng như kỳ vọng (FAIL).")