import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class SecurePage(BasePage):
    """Page object for the secure area at /secure."""

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
        """Assert the heading and logout button are visible."""

        expect(self._heading).to_be_visible()
        expect(self._logout_btn).to_be_visible()

    @allure.step("Check the success popup visibility")
    def assert_success_popup(self) -> None:
        """Assert the login success flash message is visible."""

        expect(self._success_popup).to_be_visible()
        expect(self._success_popup).to_contain_text(
            "You logged into a secure area"
        )

    @allure.step("Perform logout")
    def logout(self) -> None:
        """Click the logout button."""

        logger.info("Logging out from secure page")

        self._logout_btn.click()
