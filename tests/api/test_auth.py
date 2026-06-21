import pytest
import allure

from api.auth_client import AuthClient
from models.base import ErrorResponse
from models.auth import LoginResponse
from models.user import UserResponse
from utils.config import Users
from utils.assertions import (
    assert_status_code,
    assert_valid_schema,
    assert_valid_field,
)


@allure.feature("Authentication")
@allure.story("API login behavior")
@pytest.mark.api
@pytest.mark.regression
class TestLogin:
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_valid(self, auth_client: AuthClient) -> None:
        response = auth_client.login(Users.API_USER, Users.API_PASS)

        assert_status_code(response.status_code, 200)
        parsed = assert_valid_schema(response.json(), LoginResponse)
        assert_valid_field(parsed, "username", Users.API_USER)

    def test_login_invalid(self, auth_client: AuthClient) -> None:
        response = auth_client.login("username", "password")

        assert_status_code(response.status_code, 400)
        parsed = assert_valid_schema(response.json(), ErrorResponse)
        assert_valid_field(parsed, "message", "Invalid credentials")


@allure.feature("Authentication")
@allure.story("API get current user by token behavior")
@pytest.mark.api
@pytest.mark.regression
class TestGetAuthUser:
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_curr_user_valid(self, auth_client: AuthClient) -> None:
        token = auth_client.get_user_token(Users.API_USER, Users.API_PASS)
        response = auth_client.get_auth_user(token)

        assert_status_code(response.status_code, 200)
        parsed = assert_valid_schema(response.json(), UserResponse)
        assert_valid_field(parsed, "username", Users.API_USER)

    def test_curr_user_invalid(self, auth_client: AuthClient) -> None:
        response = auth_client.get_auth_user("")

        assert_status_code(response.status_code, 401)
        parsed = assert_valid_schema(response.json(), ErrorResponse)
        assert_valid_field(parsed, "message", "Invalid/Expired Token!")
