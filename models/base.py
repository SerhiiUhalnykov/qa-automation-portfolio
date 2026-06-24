from typing import ClassVar
from pydantic import BaseModel, model_validator


class NonEmptyBaseModel(BaseModel):
    """Pydantic model that validates _check_non_empty fields are not blank."""

    _check_non_empty: ClassVar[set[str]] = set()

    @model_validator(mode="after")
    def check_non_empty_fields(self) -> "NonEmptyBaseModel":
        """Raise ValueError if any _check_non_empty field is empty."""

        for field in self._check_non_empty:
            value = getattr(self, field)
            if value in (None, "", [], {}):
                raise ValueError(f"{field} must not be empty, got {value!r}")
        return self


class ErrorResponse(NonEmptyBaseModel):
    """Standard error response body returned by the API."""

    _check_non_empty = {"message"}

    message: str
