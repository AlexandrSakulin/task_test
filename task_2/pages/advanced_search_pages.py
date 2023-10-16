from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from task_test.task_2.pages.base_page import BasePage


class AdvancedPageLocators:
    SEARCH_INPUT_TITLE = (By.ID, "find_film")
    SEARCH_INPUT_COUNTRY = (By.ID, "country")
    SEARCH_INPUT_GENRE = (By.ID, "m_act[genre]")
    BUTTON_SEARCH = (By.CSS_SELECTOR, "input[type='button'][value='поиск']")
    MESSAGE_ERROR = (By.LINK_TEXT, "//h2[text()='К сожалению, по вашему запросу ничего не найдено...']")
    ELEMENTS_SEARCH_RESULT = (By.CLASS_NAME, "element")


class AdvancedSearchPage(BasePage, AdvancedPageLocators):
    def entering_title(self, search_params):
        self.find_element(*self.SEARCH_INPUT_TITLE).send_keys(search_params)

    def entering_country(self, search_params):
        country_dropdown = self.find_element(*self.SEARCH_INPUT_COUNTRY)
        country_dropdown.click()
        select = Select(country_dropdown)
        select.select_by_visible_text(search_params)

    def entering_genre(self, search_params):
        genre_dropdown = self.find_element(*self.SEARCH_INPUT_GENRE)
        select = Select(genre_dropdown)
        select.select_by_visible_text(search_params)

    def click_in_search(self):
        self.find_element(*self.BUTTON_SEARCH).click()

    def check_movie_in_top_5(self, title):
        elements = self.find_elements(*self.ELEMENTS_SEARCH_RESULT)
        elements = elements[:5]
        movie_to_find = title
        found = False
        for element in elements:
            if movie_to_find in element.text:
                found = True
                break

        assert found, f"Фильм '{movie_to_find}' не найден в топ 5 выдачи результата поиска"
