from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    """Базовый класс для страниц веб-приложения."""

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by: By, value: str, timeout: int = 10) -> WebElement:
        """Ищет и возвращает веб-элемент, ожидая его появления и видимости на странице."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value)), message=f"Элемент {by, value} не найден"
        )

    def find_elements(self, by: By, value: str, timeout: int = 10) -> list[WebElement]:
        """Ищет и возвращает веб-элементы, ожидая его появления их видимости на странице."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located((by, value)),
            message=f"Элементы {by, value} не найдены",
        )
