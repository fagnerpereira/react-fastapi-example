from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: Optional[str] = None
    full_name: Optional[str] = None
    hashed_password: str
    fruits: List["Fruit"] = Relationship(back_populates="user")


class Fruit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # created_at: datetime = Field(default_factory=datetime.now())
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="fruits")


class CreateFruit(BaseModel):
    name: str


class PublicUser(SQLModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class PublicFruit(SQLModel):
    id: int
    name: str
    created_at: datetime
    user_id: int
