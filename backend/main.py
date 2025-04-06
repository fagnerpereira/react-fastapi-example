import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
from itertools import count

origins = ["http://localhost:5173"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Fruit(BaseModel):
    id: int
    name: str
    created_at: datetime


class CreateFruit(BaseModel):
    name: str


class Fruits(dict):
    pass


fruits_db = Fruits(
    {
        1: Fruit(id=1, name="apple", created_at=datetime.now()),
        2: Fruit(id=2, name="banana", created_at=datetime.now()),
        3: Fruit(id=3, name="orange", created_at=datetime.now()),
    }
)
fruit_id_counter = count(4)


def get_fruits():
    return fruits_db.values()


@app.get("/fruits")
def read_fruits() -> List:
    return get_fruits()


@app.get("/fruits/{fruit_id}")
def read_fruit(fruit_id: int) -> Fruit:
    return fruits_db[fruit_id]


@app.post("/fruits")
def create_fruits(fruit: CreateFruit) -> Fruit:
    new_id = next(fruit_id_counter)
    new_fruit = Fruit(id=new_id, name=fruit.name, created_at=datetime.now())
    fruits_db[new_id] = new_fruit

    return new_fruit


@app.put("/fruits/{fruit_id}")
def update_fruit(fruit_id: int, fruit: CreateFruit) -> Fruit:
    if fruit_id in fruits_db:
        fruits_db[fruit_id].name = fruit.name
        return fruits_db[fruit_id]
    else:
        return {"error": "Fruit not found"}, 404


@app.delete("/fruits/{fruit_id}")
def delete_fruit(fruit_id: int):
    if fruit_id in fruits_db:
        name = fruits_db[fruit_id].name
        del fruits_db[fruit_id]
        return {"message": "Fruit " + name + " deleted"}
    else:
        return {"error": "Fruit not found"}, 404


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
