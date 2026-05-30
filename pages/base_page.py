import allure
from playwright.sync_api import Page

from utils.config import URL
from utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    BASE_URL: str = URL
    PATH: str = ""

    def __init__(self, page: Page) -> None:
        logger.info(f"Initializaing {self.__class__.__name__}")
        self._page: Page = page
        self._url: str = self.BASE_URL + self.PATH

    @property
    def url(self) -> str:
        return self._page.url

    @allure.step("Open page")
    def open(self) -> None:
        self._page.goto(self._url)