from .models import UserInDB, Fruit
from datetime import datetime
from itertools import count


class Database:
    def __init__(self):
        self.users = {
            "johndoe": UserInDB(
                id=1,
                username="johndoe",
                full_name="John Doe",
                email="johndoe@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            ),
            "alice": UserInDB(
                id=2,
                username="alice",
                full_name="Alice Doe",
                email="alice@example.com",
                hashed_password="$2b$12$sSe.JX82e.F7tymToom73OIX3aUtE3kYlXJrmmyJgoqJ4FNB08UnW",
            ),
        }
        self.fruits = {
            1: Fruit(id=1, name="apple", created_at=datetime.now(), user_id=1),
            2: Fruit(id=2, name="banana", created_at=datetime.now(), user_id=2),
        }
        self.fruit_id_counter = count(start=4)

    def get_user_fruits(self, id: str):
        return [fruit for fruit in self.fruits.values() if fruit.user_id == id]

    def get_user_fruit(self, id: int, user_id: int):
        fruit = self.fruits.get(id)

        if not fruit or fruit.user_id != user_id:
            return None

        return fruit

    def create_fruit(self, fruit: Fruit, user_id: int):
        new_id = next(self.fruit_id_counter)
        new_fruit = Fruit(
            id=new_id, name=fruit.name, created_at=datetime.now(), user_id=user_id
        )
        self.fruits[new_id] = new_fruit

        return new_fruit

    def update_fruit(self, id: int, updated_fruit: Fruit, user_id: int):
        fruit = self.get_user_fruit(id, user_id)
        fruit.name = updated_fruit.name

        return fruit

    def delete_fruit(self, id: int, user_id: int):
        fruit = self.get_user_fruit(id, user_id)

        if fruit:
            name = DB.fruits[id].name
            del self.fruits[id]
            return name

        return None


DB = Database()


def get_db():
    return DB
