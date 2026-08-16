from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.login_locators import LoginLocators

class LoginPage(BasePage):
    def perform_login(self, email, password):
        self.fill(LoginLocators.EMAIL_INPUT, email)
        self.fill(LoginLocators.PASSWORD_INPUT, password)
        self.click(LoginLocators.LOGIN_BUTTON)

    def verify_login_success(self):
        """Verify login success by checking the header"""
        locator = self.page.locator(LoginLocators.LOGGED_IN_TEXT)
        expect(locator).to_be_visible(timeout=5000)

    def get_login_error(self):
        """Get the red error message immediately (Fast Fail)"""
        error_locator = self.page.locator(LoginLocators.ERROR_MESSAGE).first
        try:
            if error_locator.is_visible(timeout=1500):
                return error_locator.inner_text()
        except Exception:
            pass
        return None

    def get_html5_validation_error(self):
        """Get the HTML5 tooltip error if any fields are left empty"""
        error_msg = self.page.evaluate("() => document.activeElement.validationMessage")
        return error_msg if error_msg else None