from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import Config

def test_login_valid_user(setup):
    driver = setup

    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    login_page.login(Config.EMAIL, Config.PASSWORD)

    assert dashboard_page.is_dashboard_displayed(), "Dashboard not displayed after login"
