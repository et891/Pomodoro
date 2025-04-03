from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from database import get_db_session
from models import Tasks, Categories
from schema.task import TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task(self, task_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id)
        return self.db_session.execute(query).scalar_one_or_none()

    def get_tasks(self) -> list[Tasks]:
        query = select(Tasks)
        return self.db_session.execute(query).scalars().all()

    def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        return self.db_session.execute(query).scalar_one_or_none()

    def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id
        )
        self.db_session.add(task_model)
        self.db_session.commit()
        return task_model.id

    def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = (
            update(Tasks)
            .where(Tasks.id == task_id)
            .values(name=name)
            .returning(Tasks.id)
        )
        updated_task_id: int = self.db_session.execute(query).scalar_one_or_none()
        self.db_session.commit()
        return self.get_task(updated_task_id)

    def delete_task(self, task_id: int, user_id: int) -> None:
        self.db_session.execute(delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id))
        self.db_session.commit()

    def task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = (
            select(Tasks)
            .join(Categories, Tasks.category_id == Categories.id)
            .where(Categories.name == category_name)
        )
        return self.db_session.execute(query).scalars().all()


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)
