from selenium.webdriver.common.by import By
from utilities.wait_utils import WaitUtils

class LoginPage:

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    

    def __init__(self, driver):
        self.driver = driver
        self.wait = WaitUtils(driver)

    def enter_email(self, email):
        self.wait.wait_for_element_visible(self.EMAIL_INPUT).send_keys(email)

    def enter_password(self, password):
        self.wait.wait_for_element_visible(self.PASSWORD_INPUT).send_keys(password)

    def click_login(self):
        self.wait.wait_for_element_clickable(self.LOGIN_BUTTON).click()

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
    
    