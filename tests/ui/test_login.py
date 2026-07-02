import pytest
import allure
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.secure_page import SecurePage
from data.users import Users

INVALID_LOGIN_CASES = [
    pytest.param("", Users.STAN.password, id="empty-user"),
    pytest.param("wronguser", Users.STAN.password, id="wrong-user"),
    pytest.param("wronguser", "wrongpass", id="wrong-user-pass"),
    pytest.param("", "", id="empty-user-pass"),
]
INVALID_PASS_CASES = [
    pytest.param(Users.STAN.username, "", id="empty-pass"),
    pytest.param(Users.STAN.username, "wrongpass", id="wrong-pass"),
]


@allure.feature("Authentication")
@allure.story("Login page behavior")
@pytest.mark.regression
class TestLogin:
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_full_login_logout_valid(self, page: Page) -> None:

        login_pg = LoginPage(page)
        login_pg.open()
        login_pg.assert_loaded()

        login_pg.login(Users.STAN.username, Users.STAN.password)
        secure_pg = SecurePage(page)
        secure_pg.assert_url()
        secure_pg.assert_loaded()
        secure_pg.assert_success_popup()
        secure_pg.logout()
        login_pg.assert_url()
        login_pg.assert_loaded()

    @pytest.mark.parametrize("username,password", INVALID_LOGIN_CASES)
    def test_login_invalid_username(
        self, page: Page, username: str, password: str
    ):

        login_pg = LoginPage(page)
        login_pg.open()
        login_pg.assert_loaded()

        login_pg.login(username, password)
        login_pg.assert_invalid_user_err()

    @pytest.mark.parametrize("username,password", INVALID_PASS_CASES)
    def test_login_invalid_password(
        self, page: Page, username: str, password: str
    ):

        login_pg = LoginPage(page)
        login_pg.open()
        login_pg.assert_loaded()

        login_pg.login(username, password)
        login_pg.assert_invalid_pass_err()
