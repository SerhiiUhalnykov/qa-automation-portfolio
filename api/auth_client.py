import requests

import allure

from api.base_client import BaseClient
from utils.logger import get_logger

logger = get_logger(__name__)


class AuthClient(BaseClient):
    """Client for the /auth API endpoints."""

    CLIENT_PATH: str = "/auth"

    @allure.step("Perform Login")
    def login(self, username: str, password: str) -> requests.Response:
        """Post credentials to /auth/login and return the response."""

        payload = {"username": username, "password": password}
        response = self.post("/login", json=payload)
        return response

    @allure.step("Get current auth user")
    def get_auth_user(self, token: str) -> requests.Response:
        """Fetch the authenticated user profile using a Bearer token."""

        header = {"Authorization": f"Bearer {token}"}
        return self.get("/me", headers=header)

    @allure.step("Request user token")
    def get_user_token(self, username: str, password: str) -> str:
        """Log in and return accessToken; raises ValueError if absent."""

        response = self.login(username, password)
        token = response.json().get("accessToken", "")
        if not token:
            logger.error(
                f"No access token; status: {response.status_code}"
            )
            raise ValueError("Response returned no access token")
        return token
