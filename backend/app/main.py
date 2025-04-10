import uvicorn
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
from .models import User, Fruit, CreateFruit, TokenData, Token
from .database import DB, create_db_and_tables, get_session
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os
from sqlmodel import Session

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


origins = ["http://localhost:5173"]
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    return DB.users.get(username)


def authenticate_user(username: str, password: str, session: Session):
    user = DB.get_user_by_username(session, username)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = DB.get_user_by_username(session, token_data.username)

    if user is None:
        raise credentials_exception

    return user


@app.post("/token")
async def login(
    username: str, password: str, session: Session = Depends(get_session)
) -> Token:
    user = authenticate_user(username, password, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.get("/fruits")
def read_fruits(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List:

    return DB.get_user_fruits(session, current_user.id)


@app.post("/fruits")
def create_fruits(
    fruit: CreateFruit,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Fruit:
    new_fruit = DB.create_fruit(session, fruit, current_user.id)

    return new_fruit


@app.put("/fruits/{fruit_id}")
def update_fruit(
    fruit_id: int,
    fruit: CreateFruit,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    updated_fruit = DB.update_fruit(session, fruit_id, fruit, current_user.id)

    if not updated_fruit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fruit not found"
        )

    return updated_fruit


@app.delete("/fruits/{fruit_id}")
def delete_fruit(
    fruit_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    name = DB.delete_fruit(session, fruit_id, current_user.id)

    if not name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fruit not found"
        )

    if name:
        return {"message": "Fruit " + name + " deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
