from pydantic import BaseModel


class TestUser(BaseModel):
    username: str
    password: str
