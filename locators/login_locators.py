class LoginLocators:
    EMAIL_INPUT = "[data-qa='login-email']"
    PASSWORD_INPUT = "[data-qa='login-password']"
    LOGIN_BUTTON = "[data-qa='login-button']"
    ERROR_MESSAGE = "form[action='/login'] p"
    LOGOUT_BUTTON = "a[href='/logout']"
    LOGGED_IN_TEXT = "text=Logged in as"