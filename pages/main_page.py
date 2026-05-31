import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class MainPage(BasePage):
    PATH: str = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self._heading = self._page.get_by_role("heading", name="Welcome to the-internet")

    @allure.step("Check main page is loaded")
    def should_be_loaded(self) -> None:
        
        expect(self._heading).to_be_visible()