import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
from .models import User, Fruit, CreateFruit
from .database import DB

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


def get_user(username: str):
    return DB.users.get(username)


def fake_decode_token(token):
    user = get_user(token)
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


@app.post("/token")
async def login(username: str, password: str):
    user = DB.users.get(username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/fruits")
def read_fruits(current_user: User = Depends(get_current_user)) -> List:
    return DB.get_user_fruits(current_user.id)


@app.post("/fruits")
def create_fruits(
    fruit: CreateFruit, current_user: User = Depends(get_current_user)
) -> Fruit:
    new_fruit = DB.create_fruit(fruit, current_user.id)

    return new_fruit


@app.put("/fruits/{fruit_id}")
def update_fruit(
    fruit_id: int, fruit: CreateFruit, current_user: User = Depends(get_current_user)
) -> Fruit:
    updated_fruit = DB.update_fruit(fruit_id, fruit, current_user.id)

    if not updated_fruit:
        return {"error": "Fruit not found"}, 404

    return updated_fruit


@app.delete("/fruits/{fruit_id}")
def delete_fruit(fruit_id: int, current_user: User = Depends(get_current_user)):
    name = DB.delete_fruit(fruit_id, current_user.id)

    if name:
        return {"message": "Fruit " + name + " deleted"}
    return {"error": "Fruit not found"}, 404


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
