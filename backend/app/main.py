import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Annotated
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
from itertools import count
import time

origins = ["http://localhost:5173"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(User):
    hashed_password: str


class Fruit(BaseModel):
    id: int
    name: str
    created_at: datetime


class CreateFruit(BaseModel):
    name: str


class Fruits(dict):
    pass


users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
    },
}
fruits_db = Fruits(
    {
        1: Fruit(id=1, name="apple", created_at=datetime.now()),
        2: Fruit(id=2, name="banana", created_at=datetime.now()),
        3: Fruit(id=3, name="orange", created_at=datetime.now()),
    }
)
fruit_id_counter = count(4)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(users_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_fruits():
    return fruits_db.values()


@app.post("/token")
async def login(username: str, password: str):
    user_dict = users_db.get(username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/fruits")
def read_fruits(current_user: User = Depends(get_current_user)) -> List:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return get_fruits()


@app.get("/fruits/{fruit_id}")
def read_fruit(fruit_id: int, current_user: User = Depends(get_current_user)) -> Fruit:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return fruits_db[fruit_id]


@app.post("/fruits")
def create_fruits(
    fruit: CreateFruit, current_user: User = Depends(get_current_user)
) -> Fruit:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    new_id = next(fruit_id_counter)
    new_fruit = Fruit(id=new_id, name=fruit.name, created_at=datetime.now())
    fruits_db[new_id] = new_fruit

    return new_fruit


@app.put("/fruits/{fruit_id}")
def update_fruit(
    fruit_id: int, fruit: CreateFruit, current_user: User = Depends(get_current_user)
) -> Fruit:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if fruit_id in fruits_db:
        fruits_db[fruit_id].name = fruit.name
        return fruits_db[fruit_id]
    else:
        return {"error": "Fruit not found"}, 404


@app.delete("/fruits/{fruit_id}")
def delete_fruit(fruit_id: int, current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if fruit_id in fruits_db:
        name = fruits_db[fruit_id].name
        del fruits_db[fruit_id]
        return {"message": "Fruit " + name + " deleted"}
    else:
        return {"error": "Fruit not found"}, 404


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
