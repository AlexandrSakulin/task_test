import pytest
from selenium import webdriver

from task_2.configurations import BROWSER, MAIN_URL, SCREEN_RESOLUTION


def get_firefox():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument(f"--window-size={SCREEN_RESOLUTION[0]},{SCREEN_RESOLUTION[1]}")
    return webdriver.Firefox(options=firefox_options)


def get_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--window-size={SCREEN_RESOLUTION[0]},{SCREEN_RESOLUTION[1]}")
    return webdriver.Chrome(options=chrome_options)


BROWSER_TYPE = {"chrome": get_chrome, "firefox": get_firefox}


@pytest.fixture
def browser(request):
    driver = BROWSER_TYPE[BROWSER]()
    driver.get(MAIN_URL)
    yield driver
    driver.quit()
