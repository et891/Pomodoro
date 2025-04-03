from pydantic import BaseModel, model_validator

class TaskSchema(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int
    user_id: int

    @model_validator(mode="after")
    @classmethod
    def check_pomodoro_count_or_name_is_not_None(cls, model):
        if model.name is None and model.pomodoro_count is None:
            raise ValueError("Either 'name' or 'pomodoro_count' must be provided")
        return model

    class Config:
        from_attributes = True

class TaskCreateSchema(BaseModel):
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int