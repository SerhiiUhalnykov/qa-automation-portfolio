from typing import TypeVar

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
