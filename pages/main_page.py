import allure

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class MainPage(BasePage):
    PATH: str = "/"

    @allure.step("Check main page is loaded")
    def is_loaded(self) -> bool:
        heading = self._page.get_by_role("heading", name="Welcome to the-internet")
        return heading.is_visible()