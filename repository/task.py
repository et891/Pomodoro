from sqlalchemy import select,update, delete
from sqlalchemy.orm import Session

from database import Tasks, get_db_session, Categories
from schema.task import TaskSchema


class TaskRepository:
    def __init__(self,db_session:Session):
        self.db_session = db_session

    def get_task(self, task_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id)
        task = self.db_session.execute(query).scalar_one_or_none()
        return task

    def get_tasks(self)  -> list[Tasks] :
        query = select(Tasks)
        task: list[Tasks] = self.db_session.execute(query).scalars().all()
        return task

    def create_task(self, task:TaskSchema) -> int:
        task_model = Tasks(name=task.name, pomodoro_count=task.pomodoro_count, category_id = task.category_id)
        with self.db_session as session:
            session.add(task_model)
            session.commit()
            return task_model.id

    def update_task_name(self, task_id: int, name:str) -> Tasks:
        query = update(Tasks).where(Tasks.id== task_id).values(name= name).returning(Tasks.id)
        with self.db_session as session:
            task_id : int =session.execute(query).scalar_one_or_none()
            return self.get_task(task_id)

    def delete_task(self, task_id: int) -> None:
        with self.db_session as session:
            session.execute(delete(Tasks).where(Tasks.id == task_id))
            session.commit()

    def task_by_category_name(self, category_name:str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)

def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)