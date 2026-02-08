import pytest
from selenium import webdriver
from config.config import Config

@pytest.fixture
def setup():
    if Config.BROWSER == "chrome":
        driver = webdriver.Chrome()

    driver.get(Config.BASE_URL)
    driver.maximize_window()
    driver.implicitly_wait(Config.IMPLICIT_WAIT)

    yield driver

    driver.quit()
