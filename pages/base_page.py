import allure
from playwright.sync_api import Page, expect

from utils.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    BASE_URL: str = settings.base_url
    PATH: str = ""

    def __init__(self, page: Page) -> None:
        logger.info(
            f"Initializing {self.__class__.__name__} with URL: {self._url}"
        )

        self._page: Page = page

    @property
    def _url(self) -> str:

        return self.BASE_URL + self.PATH

    def open(self) -> None:

        with allure.step(f"Open page {self.__class__.__name__}"):
            self._page.goto(self._url)

    def assert_url(self) -> None:

        with allure.step(f"Check page {self.__class__.__name__} url"):
            expect(self._page).to_have_url(self._url)
