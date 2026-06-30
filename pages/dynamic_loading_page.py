import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class DynamicLoadingPage(BasePage):
    """Page object for the /dynamic_loading endpoint."""

    PATH: str = "/dynamic_loading"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self._header = self._page.get_by_role(
            "heading", name="Dynamically Loaded Page"
        )
        self._links = self._page.get_by_role("link", name="Example")

        self._start_btn = self._page.get_by_role("button", name="Start")
        self._loading = self._page.locator("#loading")
        self._finish_text = self._page.locator("#finish")

    def open_example(self, num: int) -> None:
        """Open subpage using its endpoint"""

        self.open(f"/{num}")

    @allure.step("Start dynamic loading")
    def start_loading(self) -> None:

        self._start_btn.click()

    @allure.step("Check dynamic loading page is loaded")
    def assert_loaded(self) -> None:
        """Assert DynamicLoadingPage elements are visible."""

        expect(self._header).to_be_visible()
        expect(self._links).to_have_count(2)
        for el in self._links.all():
            expect(el).to_be_visible()

    @allure.step("Check loading indicator appears and disappears")
    def assert_loading_then_done(self, timeout: int) -> None:
        """Assert loading indicator appears and dissapears before timeout."""

        expect(self._loading).to_be_visible()
        expect(self._loading).to_be_hidden(timeout=timeout)

    @allure.step("Check final text is visible")
    def assert_finish_text(self) -> None:
        """Assert finish text is visible and contains correct text."""

        expect(self._finish_text).to_be_visible()
        expect(self._finish_text).to_contain_text("Hello World!")
