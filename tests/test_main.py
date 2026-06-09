import pytest
import allure
from playwright.sync_api import Page

from pages.main_page import MainPage


@allure.story("Main page behavior")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_main(page: Page) -> None:
    main = MainPage(page)
    main.open()
    main.assert_loaded()
