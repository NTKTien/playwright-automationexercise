class RegisterLocators:
    # Bước 1
    SIGNUP_NAME = "[data-qa='signup-name']"
    SIGNUP_EMAIL = "[data-qa='signup-email']"
    SIGNUP_BUTTON = "[data-qa='signup-button']"
    SIGNUP_ERROR = "form[action='/signup'] p"
    
    # Bước 2
    TITLE_MR = "#id_gender1"
    ACCOUNT_NAME = "[data-qa='name']"          
    ACCOUNT_EMAIL = "[data-qa='email']"        
    PASSWORD = "[data-qa='password']"
    FIRST_NAME = "[data-qa='first_name']"
    LAST_NAME = "[data-qa='last_name']"
    ADDRESS = "[data-qa='address']"
    STATE = "[data-qa='state']"
    CITY = "[data-qa='city']"
    ZIPCODE = "[data-qa='zipcode']"
    MOBILE_NUMBER = "[data-qa='mobile_number']"
    CREATE_ACCOUNT_BTN = "[data-qa='create-account']"
    
    # Bước 3
    ACCOUNT_CREATED_MSG = "[data-qa='account-created']"
    CONTINUE_BTN = "[data-qa='continue-button']"
    LOGGED_IN_TEXT = "ul.nav li a:has-text('Logged in as')"
    
    # Bước 4
    DELETE_ACCOUNT_BTN = "a[href='/delete_account']"
    ACCOUNT_DELETED_MSG = "[data-qa='account-deleted']"