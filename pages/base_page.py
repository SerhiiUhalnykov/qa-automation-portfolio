import allure
from playwright.sync_api import Page, Response, expect

from utils.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """Base page object with URL navigation and assertion helpers."""

    BASE_URL: str = settings.base_url
    PATH: str = ""

    def __init__(self, page: Page) -> None:
        logger.info(
            f"Initializing {self.__class__.__name__} with URL: {self._url}"
        )

        self._page: Page = page

    @property
    def _url(self) -> str:
        """Full URL for this page."""

        return self.BASE_URL + self.PATH

    def open(self, sub_path: str = "") -> Response | None:
        """Navigate to this page's URL."""

        url = f"{self._url}{sub_path}"
        logger.info(f"Opening {url}")
        with allure.step(f"Open page {self.__class__.__name__}"):
            return self._page.goto(f"{url}")

    def assert_url(self) -> None:
        """Assert the browser is currently at this page's URL."""

        with allure.step(f"Check page {self.__class__.__name__} url"):
            expect(self._page).to_have_url(self._url)
