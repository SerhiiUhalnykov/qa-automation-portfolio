import requests

import allure

from utils.logger import get_logger
from utils.config import settings

logger = get_logger(__name__)


class BaseClient:
    BASE_URL: str = settings.api_url
    CLIENT_PATH: str = ""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.last_response: requests.Response | None = None

        logger.info(
            f"Initializing {self.__class__.__name__} with URL: {self.client_url}"
        )

    @property
    def client_url(self) -> str:
        return f"{self.BASE_URL}{self.CLIENT_PATH}"

    @allure.step("Perform GET request")
    def get(self, path: str = "", **kwargs) -> requests.Response:
        self.last_response = self.session.get(
            f"{self.client_url}{path}", **kwargs
        )
        return self.last_response

    @allure.step("Perform POST request")
    def post(self, path: str, **kwargs) -> requests.Response:
        self.last_response = self.session.post(
            f"{self.client_url}{path}", **kwargs
        )
        return self.last_response

    @allure.step("Perform PUT request")
    def put(self, path: str, **kwargs) -> requests.Response:
        self.last_response = self.session.put(
            f"{self.client_url}{path}", **kwargs
        )
        return self.last_response

    @allure.step("Perform PATCH request")
    def patch(self, path: str, **kwargs) -> requests.Response:
        self.last_response = self.session.patch(
            f"{self.client_url}{path}", **kwargs
        )
        return self.last_response

    @allure.step("Perform DELETE request")
    def delete(self, path: str, **kwargs) -> requests.Response:
        self.last_response = self.session.delete(
            f"{self.client_url}{path}", **kwargs
        )
        return self.last_response

    @allure.step("Authorize client session")
    def authorize_session(self, token: str) -> None:
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def close(self) -> None:
        self.session.close()
