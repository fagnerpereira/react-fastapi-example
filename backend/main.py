from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Fruit(BaseModel):
    name: str


class Fruits(BaseModel):
    fruits: List


fruits_db = Fruits(
    fruits=[
        Fruit(name="apple"),
        Fruit(name="banana"),
        Fruit(name="orange"),
    ]
)


@app.get("/fruits")
def get_fruits():
    return fruits_db
