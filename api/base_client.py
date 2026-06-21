import requests

import allure

from utils.logger import get_logger
from utils.config import API_URL

logger = get_logger(__name__)


class BaseClient:
    def __init__(self, base_url: str = API_URL) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.last_response: requests.Response | None = None

        logger.info(
            f"Initializing {self.__class__.__name__} with URL: {self.base_url}"
        )

    @allure.step("Perform GET request")
    def get(self, path: str, **kwargs) -> requests.Response:
        self.last_response = self.session.get(
            f"{self.base_url}{path}", **kwargs
        )
        return self.last_response

    @allure.step("Perform POST request")
    def post(self, path: str, **kwargs) -> requests.Response:
        self.last_response = self.session.post(
            f"{self.base_url}{path}", **kwargs
        )
        return self.last_response

    @allure.step("Perform PUT request")
    def put(self, path: str, **kwargs) -> requests.Response:
        self.last_response = self.session.put(
            f"{self.base_url}{path}", **kwargs
        )
        return self.last_response

    @allure.step("Perform DELETE request")
    def delete(self, path: str, **kwargs) -> requests.Response:
        self.last_response = self.session.delete(
            f"{self.base_url}{path}", **kwargs
        )
        return self.last_response

    @allure.step("Authorize client session")
    def authorize_session(self, token: str) -> None:
        self.session.headers.update({"Authorization": f"Brearer {token}"})

    def close(self) -> None:
        self.session.close()
