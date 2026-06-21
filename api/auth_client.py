import requests

import allure

from api.base_client import BaseClient


class AuthClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.base_url += "/auth"

    @allure.step("Perform Login")
    def login(self, username: str, password: str) -> requests.Response:
        payload = {"username": username, "password": password}
        response = self.post("/login", json=payload)
        return response

    @allure.step("Get current auth user")
    def get_auth_user(self, token: str) -> requests.Response:
        header = {"Authorization": f"Bearer {token}"}
        return self.get("/me", headers=header)

    @allure.step("Request user token")
    def get_user_token(self, username: str, password: str) -> str:
        response = self.login(username, password)
        token = response.json().get("accessToken", "")
        if not token:
            raise ValueError("Response returned no access token")
        return token
