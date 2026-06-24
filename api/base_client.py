import requests

import allure

from utils.logger import get_logger
from utils.config import settings

logger = get_logger(__name__)


class BaseClient:
    """Base HTTP client using requests.Session; subclasses add endpoints."""

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
        """Full base URL for this client."""

        return f"{self.BASE_URL}{self.CLIENT_PATH}"

    @allure.step("Perform GET request")
    def get(self, path: str = "", **kwargs) -> requests.Response:
        """Send a GET request to client_url + path."""

        url = f"{self.client_url}{path}"
        self.last_response = self.session.get(url, **kwargs)
        logger.info(f"GET {url} -> {self.last_response.status_code}")
        return self.last_response

    @allure.step("Perform POST request")
    def post(self, path: str, **kwargs) -> requests.Response:
        """Send a POST request to client_url + path."""

        url = f"{self.client_url}{path}"
        self.last_response = self.session.post(url, **kwargs)
        logger.info(f"POST {url} -> {self.last_response.status_code}")
        return self.last_response

    @allure.step("Perform PUT request")
    def put(self, path: str, **kwargs) -> requests.Response:
        """Send a PUT request to client_url + path."""

        url = f"{self.client_url}{path}"
        self.last_response = self.session.put(url, **kwargs)
        logger.info(f"PUT {url} -> {self.last_response.status_code}")
        return self.last_response

    @allure.step("Perform PATCH request")
    def patch(self, path: str, **kwargs) -> requests.Response:
        """Send a PATCH request to client_url + path."""

        url = f"{self.client_url}{path}"
        self.last_response = self.session.patch(url, **kwargs)
        logger.info(f"PATCH {url} -> {self.last_response.status_code}")
        return self.last_response

    @allure.step("Perform DELETE request")
    def delete(self, path: str, **kwargs) -> requests.Response:
        """Send a DELETE request to client_url + path."""

        url = f"{self.client_url}{path}"
        self.last_response = self.session.delete(url, **kwargs)
        logger.info(f"DELETE {url} -> {self.last_response.status_code}")
        return self.last_response

    @allure.step("Authorize client session")
    def authorize_session(self, token: str) -> None:
        """Set a Bearer token on the session for all subsequent requests."""

        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def close(self) -> None:
        """Close the underlying requests session."""

        self.session.close()
