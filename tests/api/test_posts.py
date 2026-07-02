import pytest
import allure
from faker import Faker

from api.posts_client import PostsClient
from models.base import ErrorResponse
from models.post import PostResponse, PostsResponse, PostRequest
from utils.assertions import (
    assert_status_code,
    assert_valid_schema,
    assert_valid_field,
    assert_response_contains_payload,
)

fake = Faker()


@allure.feature("Posts")
@allure.story("API posts access")
@pytest.mark.api
@pytest.mark.regression
class TestGetPosts:
    @pytest.mark.smoke
    @pytest.mark.parametrize("post_id", [1, 150, 251])
    def test_get_single_post(
        self, posts_client: PostsClient, post_id: int
    ) -> None:
        response = posts_client.get_post(post_id)

        assert_status_code(response.status_code, 201)
        parsed = assert_valid_schema(response.json(), PostResponse)
        assert_valid_field(parsed, "id", post_id)

    @pytest.mark.smoke
    def test_get_all_posts(self, posts_client: PostsClient) -> None:
        response = posts_client.get_all_posts()

        assert_status_code(response.status_code, 200)
        parsed = assert_valid_schema(response.json(), PostsResponse)

        assert len(parsed.posts) == parsed.limit, (
            f"Expected posts list length: {parsed.limit}, got: {len(parsed.posts)}"
        )

    @pytest.mark.parametrize("post_id", [0, 252])
    def test_get_single_post_invalid(
        self, posts_client: PostsClient, post_id: int
    ) -> None:
        response = posts_client.get_post(post_id)

        assert_status_code(response.status_code, 404)
        parsed = assert_valid_schema(response.json(), ErrorResponse)
        assert_valid_field(
            parsed, "message", f"Post with id '{post_id}' not found"
        )


@allure.feature("Posts")
@allure.story("API posts CRUD")
@pytest.mark.api
@pytest.mark.regression
class TestPostsCRUD:
    @pytest.mark.smoke
    def test_create_post(self, authed_posts_client: PostsClient) -> None:
        payload = PostRequest(
            userId=fake.random_int(1, 208),
            title=fake.sentence(),
            body=fake.sentence(),
            tags=[fake.word()],
        )
        response = authed_posts_client.create_post(payload)

        assert_status_code(response.status_code, 201)
        body = response.json()
        assert_valid_schema(body, PostResponse)
        assert_response_contains_payload(body, payload)

    @pytest.mark.smoke
    def test_update_post_full(self, authed_posts_client: PostsClient) -> None:
        payload = PostRequest(
            userId=fake.random_int(1, 208),
            title=fake.sentence(),
            body=fake.sentence(),
            tags=[fake.word()],
        )
        response = authed_posts_client.update_post_full(1, payload)

        assert_status_code(response.status_code, 200)
        body = response.json()
        assert_response_contains_payload(body, payload)

    def test_update_post_partial(
        self, authed_posts_client: PostsClient
    ) -> None:
        original = PostResponse.model_validate(
            authed_posts_client.get_post(1).json()
        )

        payload = PostRequest(title=fake.sentence())
        response = authed_posts_client.update_post_partial(1, payload)

        body = response.json()
        expected = original.model_copy(
            update={
                "title": payload.title,
                "reactions": None,
                "views": None,
            }
        )

        assert_status_code(response.status_code, 200)
        assert_response_contains_payload(body, expected)

    @pytest.mark.smoke
    def test_delete_post(self, authed_posts_client: PostsClient) -> None:
        response = authed_posts_client.delete_post(1)

        assert_status_code(response.status_code, 200)
        parsed = assert_valid_schema(response.json(), PostResponse)
        assert_valid_field(parsed, "id", 1)
        assert_valid_field(parsed, "isDeleted", True)

    def test_create_post_invalid(
        self, authed_posts_client: PostsClient
    ) -> None:
        payload = PostRequest(
            title=fake.sentence(),
            body=fake.sentence(),
            tags=[fake.word()],
        )
        response = authed_posts_client.create_post(payload)

        assert_status_code(response.status_code, 400)
        parsed = assert_valid_schema(response.json(), ErrorResponse)
        assert_valid_field(parsed, "message", "User id is required")
