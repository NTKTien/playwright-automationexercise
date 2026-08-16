class LoginLocators:
    EMAIL_INPUT = "[data-qa='login-email']"
    PASSWORD_INPUT = "[data-qa='login-password']"
    LOGIN_BUTTON = "[data-qa='login-button']"
    ERROR_MESSAGE = "form[action='/login'] p"
    LOGGED_IN_TEXT = "ul.nav li a:has-text('Logged in as')"
    LOGOUT_BUTTON = "a[href='/logout']"