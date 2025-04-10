from .models import User, Fruit, CreateFruit
from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from typing import Generator, Optional, List
import os

load_dotenv()

SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL")

engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


class SQLiteDatabase:
    def __init__(self):
        # Initialize the database and seed initial data
        create_db_and_tables()
        self._seed_initial_data()

    def _seed_initial_data(self):
        with Session(engine) as session:
            # Check if we have users
            user_exists = session.exec(select(User)).first() is not None

            if not user_exists:
                # Create initial users
                users = [
                    User(
                        username="johndoe",
                        full_name="John Doe",
                        email="johndoe@example.com",
                        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                    ),
                    User(
                        username="alice",
                        full_name="Alice Doe",
                        email="alice@example.com",
                        hashed_password="$2b$12$sSe.JX82e.F7tymToom73OIX3aUtE3kYlXJrmmyJgoqJ4FNB08UnW",
                    ),
                ]
                session.add_all(users)
                session.commit()

                # Refresh to get IDs
                for user in users:
                    session.refresh(user)

                # Create initial fruits
                fruits = [
                    Fruit(name="apple", created_at=datetime.now(), user_id=users[0].id),
                    Fruit(
                        name="banana", created_at=datetime.now(), user_id=users[1].id
                    ),
                ]
                session.add_all(fruits)
                session.commit()

    def get_user_by_username(self, session: Session, username: str) -> Optional[User]:
        return session.exec(select(User).where(User.username == username)).first()

    def get_user_fruits(self, session: Session, user_id: int) -> List[Fruit]:
        return session.exec(select(Fruit).where(Fruit.user_id == user_id)).all()

    def get_user_fruit(
        self, session: Session, fruit_id: int, user_id: int
    ) -> Optional[Fruit]:
        return session.exec(
            select(Fruit).where(Fruit.id == fruit_id, Fruit.user_id == user_id)
        ).first()

    def create_fruit(self, session: Session, fruit: CreateFruit, user_id: int) -> Fruit:
        new_fruit = Fruit(name=fruit.name, created_at=datetime.now(), user_id=user_id)
        session.add(new_fruit)
        session.commit()
        session.refresh(new_fruit)

        return new_fruit

    def update_fruit(
        self, session: Session, id: int, updated_fruit: CreateFruit, user_id: int
    ) -> Optional[Fruit]:
        fruit = self.get_user_fruit(session, id, user_id)

        if not fruit:
            return None

        for key, value in updated_fruit.model_dump(exclude_unset=True).items():
            setattr(fruit, key, value)

        session.add(fruit)
        session.commit()
        session.refresh(fruit)

        return fruit

    def delete_fruit(self, session: Session, id: int, user_id: int) -> Optional[str]:
        fruit = self.get_user_fruit(session, id, user_id)

        if not fruit:
            return None

        fruit_name = fruit.name

        session.delete(fruit)
        session.commit()

        return fruit_name


DB = SQLiteDatabase()
