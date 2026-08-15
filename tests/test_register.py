import pytest
from playwright.sync_api import expect
from pages.register_page import RegisterPage
from locators.register_locators import RegisterLocators
from utils.excel_utils import load_excel_data
from config.config import DATA_FILE
from utils.logger import get_logger

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
    # BƯỚC 1: XỬ LÝ FORM LOGIN/SIGNUP BAN ĐẦU
    # =======================================================
    register_page.navigate("/login")
    register_page.fill_initial_signup(case.get("SignupName"), case.get("SignupEmailAddress"))
    
    system_error = register_page.get_system_error()
    html5_error = register_page.get_html5_validation_error()
    
    if system_error or html5_error:
        error_msg = system_error or html5_error
        logger.info(f"Bắt được lỗi ở bước 1: '{error_msg}'")
        if expected_result == "FAIL":
            assert True, f"Pass đúng kỳ vọng FAIL với lỗi: {error_msg}"
            return
        else:
            pytest.fail(f"Kỳ vọng SUCCESS nhưng gặp lỗi: '{error_msg}'")

    # =======================================================
    # BƯỚC 2: ĐIỀN THÔNG TIN TÀI KHOẢN CHI TIẾT
    # =======================================================
    try:
        register_page.fill_account_details(case)
    except Exception as e:
        if expected_result == "FAIL":
            logger.info("Không thể điền form (Pass đúng kỳ vọng FAIL).")
            return
        else:
            pytest.fail(f"Lỗi khi điền thông tin Account Details: {str(e)}")

    form_error = register_page.get_html5_validation_error()
    if form_error:
        logger.info(f"Bắt được lỗi validation form: '{form_error}'")
        if expected_result == "FAIL":
            assert True
            return
        else:
            pytest.fail(f"Kỳ vọng SUCCESS nhưng form báo lỗi: '{form_error}'")

    # =======================================================
    # BƯỚC 3: XÁC NHẬN KẾT QUẢ & LUÔN DỌN DẸP (TEARDOWN)
    # =======================================================
    is_created = page.locator(RegisterLocators.ACCOUNT_CREATED_MSG).is_visible(timeout=3000)

    if is_created:
        # Nhấn Continue để vào trang chủ (nơi chứa nút Delete Account)
        register_page.click(RegisterLocators.CONTINUE_BTN)
        expected_name = case.get("AccountName") or case.get("SignupName")
        
        # Nếu test case thuộc luồng SUCCESS, tiến hành verify Header
        verify_error = None
        if expected_result == "SUCCESS":
            try:
                register_page.verify_logged_in_as(expected_name)
            except Exception as e:
                verify_error = e
                
        # LUÔN LUÔN DỌN DẸP TÀI KHOẢN (Bất kể kỳ vọng ban đầu là gì)
        try:
            register_page.delete_account()
            logger.info(f"Đã tự động dọn dẹp: Xóa tài khoản '{expected_name}' thành công.")
        except Exception as e:
            logger.error(f"Không thể xóa tài khoản để dọn dẹp: {e}")
            
        # Phán quyết (Assertion) Test Case sau khi đã dọn dẹp
        if expected_result == "FAIL":
            pytest.fail("Bug Hệ Thống: Kỳ vọng FAIL nhưng tài khoản lại được tạo thành công (Đã tự động xóa tài khoản này).")
        elif verify_error:
            pytest.fail(f"Tạo tài khoản thành công nhưng lỗi hiển thị Header: {verify_error}")
        else:
            logger.info("Đăng ký thành công và hiển thị tên đầy đủ trên header.")

    else:
        # Tài khoản không được tạo
        if expected_result == "SUCCESS":
            pytest.fail("Kỳ vọng SUCCESS nhưng tài khoản không được tạo.")
        else:
            logger.info("Pass: Hệ thống chặn tạo tài khoản đúng kỳ vọng (FAIL).")