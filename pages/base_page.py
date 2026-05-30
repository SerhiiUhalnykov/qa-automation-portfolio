import allure
from playwright.sync_api import Page

from utils.config import BASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    BASE_URL: str = BASE_URL
    PATH: str = ""

    def __init__(self, page: Page) -> None:
        logger.info(f"Initializaing {self.__class__.__name__}")
        self._page: Page = page
        self._url: str = self.BASE_URL + self.PATH

    def open(self) -> None:
        with allure.step(f"Open page {self.__class__.__name__}"):
            self._page.goto(self._url)