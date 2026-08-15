from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.login_locators import LoginLocators

class LoginPage(BasePage):
    def perform_login(self, email, password):
        self.fill(LoginLocators.EMAIL_INPUT, email)
        self.fill(LoginLocators.PASSWORD_INPUT, password)
        self.click(LoginLocators.LOGIN_BUTTON)

    def verify_login_success(self):
        expect(self.page.locator(LoginLocators.LOGGED_IN_TEXT)).to_be_visible()

    def verify_login_failed(self, error_text):
        expect(self.page.locator(LoginLocators.ERROR_MESSAGE)).to_contain_text(error_text)