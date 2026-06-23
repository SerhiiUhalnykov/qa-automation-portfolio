import pytest
import allure

from api.posts_client import PostsClient
from utils.assertions import assert_response_time


@allure.feature("Posts")
@allure.story("Response time assessment")
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.performance
def test_response_time(posts_client: PostsClient) -> None:
    response = posts_client.get_post(1)
    assert_response_time(response)
