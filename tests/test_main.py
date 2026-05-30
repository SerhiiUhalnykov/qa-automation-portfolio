import pytest
import allure
from playwright.sync_api import Page

from pages.main_page import MainPage
from utils.config import URL

@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_main(page: Page) -> None:
    main = MainPage(page)
    main.open()
    assert (URL + '/') == main.url
    assert main.is_loaded()