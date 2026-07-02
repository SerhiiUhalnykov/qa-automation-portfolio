import pytest
import allure
from playwright.sync_api import Page

from pages.main_page import MainPage


@allure.feature("Main")
@allure.story("Main page behavior")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
@pytest.mark.regression
class TestMainPage:
    def test_main(self, page: Page) -> None:
        main = MainPage(page)
        main.open()
        main.assert_loaded()
