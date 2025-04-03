from dataclasses import dataclass
from sqlalchemy.orm import Session
from models import UserProfile
from sqlalchemy import insert, select

@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, username: str, password: str) -> UserProfile:
        query = insert(UserProfile).values(
            username=username,
            password=password
        ).returning(UserProfile.id)

        result = self.db_session.execute(query)
        user_id: int = result.scalar_one()
        self.db_session.commit()  # 💾 обязательно сохраняем изменения

        return self.get_user(user_id)

    def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        result = self.db_session.execute(query)
        return result.scalar_one_or_none()

    def get_user_by_username(self, username) -> UserProfile| None:
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()

