import json

import allure
import pytest

from task_test.task_2.pages.advanced_search_pages import AdvancedSearchPage

# Загрузка параметров поиска из JSON-файла
with open("search_params.json", "r", encoding="utf-8") as file:
    movies = json.load(file)
search_params = [(movie["title"], movie["country"], movie["genre"]) for movie in movies]


@pytest.mark.parametrize("title,country,genre", search_params)
def test_advanced_search(browser, title, country, genre):
    """Тест для продвинутого поиска фильмов."""
    advanced_page = AdvancedSearchPage(browser)

    with allure.step(f"Ввод названия: {title}"):
        advanced_page.entering_title(title)
    allure.attach(browser.get_screenshot_as_png(), name=f"step_1_{title}", attachment_type=allure.attachment_type.PNG)

    with allure.step(f"Ввод страны: {country}"):
        advanced_page.entering_country(country)
    allure.attach(browser.get_screenshot_as_png(), name=f"step_2_{title}", attachment_type=allure.attachment_type.PNG)

    with allure.step(f"Ввод жанра: {genre}"):
        advanced_page.entering_genre(genre)
    allure.attach(browser.get_screenshot_as_png(), name=f"step_3_{title}", attachment_type=allure.attachment_type.PNG)

    with allure.step("Нажатие на кнопку 'Поиск'"):
        advanced_page.click_in_search()
    allure.attach(browser.get_screenshot_as_png(), name=f"step_4_{title}", attachment_type=allure.attachment_type.PNG)

    with allure.step(f"Проверка, что {title} в топ-5"):
        advanced_page.check_movie_in_top_5(title)

    movie_info = f"Фильм: {title}, Страна: {country}, Жанр: {genre}"
    allure.attach(movie_info, name=f"Информация_{title}", attachment_type=allure.attachment_type.TEXT)
    allure.attach(browser.get_screenshot_as_png(), name=f"step_5_{title}", attachment_type=allure.attachment_type.PNG)
