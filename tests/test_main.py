import pytest
import allure
from playwright.sync_api import Page

from pages.main_page import MainPage

@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_main(page: Page) -> None:
    main = MainPage(page)
    main.open()
    main.is_loaded()