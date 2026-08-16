from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.register_locators import RegisterLocators

class RegisterPage(BasePage):
    def fill_initial_signup(self, name, email):
        self.fill(RegisterLocators.SIGNUP_NAME, name)
        self.fill(RegisterLocators.SIGNUP_EMAIL, email)
        self.click(RegisterLocators.SIGNUP_BUTTON)

    def get_system_error(self):
        """Get the system error message returned by the server (e.g., duplicate email) with the fastest speed"""
        # Find the exact p tag containing the error text.
        # Using .filter(has_text=...) helps bypass Strict Mode errors completely.
        error_locator = self.page.locator("p").filter(has_text="already exist")
        
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

    def fill_account_details(self, data: dict):
        # Wait for the form to appear. If we reach here, the first step is complete.
        self.page.wait_for_selector(RegisterLocators.CREATE_ACCOUNT_BTN)
        self.click(RegisterLocators.TITLE_MR)
        
        # If account name is empty, it will type an empty string to clear the field.
        self.fill(RegisterLocators.ACCOUNT_NAME, data.get("AccountName"))
            
        email_locator = self.page.locator(RegisterLocators.ACCOUNT_EMAIL)
        expected_email = data.get("AccountEmailAddress") or data.get("SignupEmailAddress")
        if expected_email:
            expect(email_locator).to_have_value(str(expected_email))
            expect(email_locator).to_be_disabled()
                
        # Other fields
        self.fill(RegisterLocators.PASSWORD, data.get("Password"))
        self.fill(RegisterLocators.FIRST_NAME, data.get("FirstName"))
        self.fill(RegisterLocators.LAST_NAME, data.get("LastName"))
        self.fill(RegisterLocators.ADDRESS, data.get("Address"))
        self.fill(RegisterLocators.STATE, data.get("State"))
        self.fill(RegisterLocators.CITY, data.get("City"))
        self.fill(RegisterLocators.ZIPCODE, data.get("Zipcode"))
        self.fill(RegisterLocators.MOBILE_NUMBER, data.get("MobileNumber"))
        
        self.click(RegisterLocators.CREATE_ACCOUNT_BTN)

    def complete_registration(self):
        expect(self.page.locator(RegisterLocators.ACCOUNT_CREATED_MSG)).to_be_visible()
        self.click(RegisterLocators.CONTINUE_BTN)

    def verify_logged_in_as(self, expected_name):
        locator = self.page.locator(RegisterLocators.LOGGED_IN_TEXT)
        expect(locator).to_be_visible()
        expect(locator).to_contain_text(expected_name)

    def delete_account(self):
        """Clean up the account after successful testing"""
        self.click(RegisterLocators.DELETE_ACCOUNT_BTN)
        expect(self.page.locator(RegisterLocators.ACCOUNT_DELETED_MSG)).to_be_visible(timeout=5000)
        self.click(RegisterLocators.CONTINUE_BTN)