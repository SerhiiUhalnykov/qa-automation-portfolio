import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    PATH: str = "/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self._heading = self._page.get_by_role("heading", name="Login Page")

        self._username_input = self._page.get_by_role("textbox", name="Username")
        self._password_input = self._page.get_by_role("textbox", name="Password")
        self._login_btn = self._page.get_by_role("button", name="Login")

        self._invalid_err = self._page.locator("#flash")

    @allure.step("Check login page is loaded")
    def assert_loaded(self) -> None:

        expect(self._heading).to_be_visible()
        expect(self._username_input).to_be_visible()
        expect(self._password_input).to_be_visible()
        expect(self._login_btn).to_be_visible()

    @allure.step("Perform Login")
    def login(self, username: str, password: str) -> None:
        logger.info("Logging into secure page")

        self._username_input.fill(username)
        self._password_input.fill(password)
        self._login_btn.click()

    @allure.step("Check invalid username error visibility")
    def assert_invalid_user_err(self) -> None:

        expect(self._invalid_err).to_contain_text("Your username is invalid!")
        expect(self._invalid_err).to_be_visible()

    @allure.step("Check invalid password error visibility")
    def assert_invalid_pass_err(self) -> None:

        expect(self._invalid_err).to_contain_text("Your password is invalid!")
        expect(self._invalid_err).to_be_visible()
