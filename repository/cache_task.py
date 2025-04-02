import json
from redis import Redis
from schema.task import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[TaskSchema] | None:
        tasks_json = self.redis.lrange("tasks", 0, -1)
        if not tasks_json:
            return None
        return [TaskSchema.model_validate(json.loads(task)) for task in tasks_json]

    def set_tasks(self, tasks: list[TaskSchema]):
        self.redis.delete("tasks")  # очищаем, чтобы не было дублей
        for task in tasks:
            self.redis.rpush("tasks", task.json())  # rpush сохраняет порядок

    def clear_tasks(self):
        self.redis.delete("tasks")