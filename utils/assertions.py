from typing import TypeVar, Any

import allure
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@allure.step("Validate response status code")
def assert_status_code(code: int, expected: int) -> None:
    assert code == expected, (
        f"Expected status code: {expected}, received: {code}"
    )


@allure.step("Validate response schema")
def assert_valid_schema(body: dict, model: type[T]) -> T:
    return model.model_validate(body)


@allure.step("Validate field")
def assert_valid_field(model: BaseModel, field: str, expected: object) -> None:
    value = getattr(model, field)
    assert value == expected, f"Expected {field}={expected!r}, got {value!r}"


@allure.step("Validate response contains payload")
def assert_response_contains_payload(
    body: dict[str, Any], model: BaseModel
) -> None:
    for key, value in model.model_dump(exclude_none=True).items():
        assert body.get(key) == value, (
            f"{key}: expected {value!r}, got {body.get(key)!r}"
        )
