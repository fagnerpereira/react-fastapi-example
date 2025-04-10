from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    username: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(User):
    hashed_password: str


class Fruit(BaseModel):
    id: int
    name: str
    created_at: datetime
    user_id: int


class Fruits(dict):
    pass


class CreateFruit(BaseModel):
    name: str
