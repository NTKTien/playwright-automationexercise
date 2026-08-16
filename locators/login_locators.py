class LoginLocators:
    EMAIL_INPUT = "[data-qa='login-email']"
    PASSWORD_INPUT = "[data-qa='login-password']"
    LOGIN_BUTTON = "[data-qa='login-button']"
    
    # Bắt câu thông báo lỗi chữ đỏ khi sai email/pass
    ERROR_MESSAGE = "form[action='/login'] p"
    
    # Text hiển thị trên header khi đăng nhập thành công
    LOGGED_IN_TEXT = "ul.nav li a:has-text('Logged in as')"
    
    # Logout (nếu cần dùng)
    LOGOUT_BUTTON = "a[href='/logout']"