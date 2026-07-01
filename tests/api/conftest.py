from typing import Iterator
from pathlib import Path
import json

import pytest
import allure

from api.auth_client import AuthClient
from api.base_client import BaseClient
from api.user_client import UserClient
from api.posts_client import PostsClient
from utils.logger import get_logger
from data.users import Users

logger = get_logger(__name__)


@pytest.fixture(autouse=True)
def allure_markings() -> None:
    """Tag each test with 'api' as the Allure environment parameter."""

    allure.dynamic.parameter("environment", "api")
    allure.dynamic.parent_suite("API")


@pytest.fixture(scope="session")
def artifacts_subdir() -> str:
    """Return 'api' as the API artifacts subdirectory."""

    return "api"


@pytest.fixture
def auth_client() -> Iterator[AuthClient]:
    """Yield an AuthClient instance, closed after each test."""

    client = AuthClient()
    yield client
    client.close()


@pytest.fixture
def posts_client() -> Iterator[PostsClient]:
    """Yield a PostsClient instance, closed after each test."""

    client = PostsClient()
    yield client
    client.close()


@pytest.fixture
def authed_user_client(auth_client: AuthClient) -> Iterator[UserClient]:
    """Yield a UserClient pre-authorized with the API user token."""

    token = auth_client.get_user_token(Users.API.username, Users.API.password)
    client = UserClient()
    client.authorize_session(token)
    yield client
    client.close()


@pytest.fixture
def authed_posts_client(auth_client: AuthClient) -> Iterator[PostsClient]:
    """Yield a PostsClient pre-authorized with the API user token."""

    token = auth_client.get_user_token(Users.API.username, Users.API.password)
    client = PostsClient()
    client.authorize_session(token)
    yield client
    client.close()


@pytest.fixture(autouse=True)
def save_attach_results(
    request: pytest.FixtureRequest,
    artifacts_path: Path,
) -> Iterator[None]:
    """Save last API response as a JSON artifact on test failure and attach it
    to Allure report.

    Args:
        request (FixtureRequest): pytest request object for test status;
        artifacts_path (Path): a path for artifact files.
    """

    yield
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        for value in request.node.funcargs.values():
            if (
                isinstance(value, BaseClient)
                and value.last_response is not None
            ):
                response_path = Path(f"{artifacts_path}.json")

                logger.info(
                    f"Saving artifacts on failed test: {response_path.name}"
                )
                response = value.last_response
                try:
                    body = response.json()
                except ValueError:
                    body = response.text

                data = {
                    "url": response.request.url,
                    "method": response.request.method,
                    "status_code": response.status_code,
                    "body": body,
                }

                with open(response_path, "w") as file:
                    json.dump(data, file, indent=2)
                allure.attach.file(
                    response_path,
                    name="failure_response",
                    attachment_type=allure.attachment_type.JSON,
                )
