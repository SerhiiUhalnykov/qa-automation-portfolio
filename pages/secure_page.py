import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class SecurePage(BasePage):
    PATH: str = "/secure"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self._heading = self._page.get_by_role(
            "heading", name="Secure Area", exact=True
        )

        self._logout_btn = self._page.get_by_role("link", name="Logout")
        self._success_popup = self._page.locator("#flash")

    @allure.step("Check secure page is loaded")
    def assert_loaded(self) -> None:

        expect(self._heading).to_be_visible()
        expect(self._logout_btn).to_be_visible()

    @allure.step("Check the success popup visibility")
    def assert_success_popup(self) -> None:

        expect(self._success_popup).to_contain_text("You logged into a secure area")
        expect(self._success_popup).to_be_visible()

    @allure.step("Perform logout")
    def logout(self) -> None:
        logger.info("Logging out from secure page")

        self._logout_btn.click()
