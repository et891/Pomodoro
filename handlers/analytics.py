from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/tasks")
async def get_tasks():
    return []

@router.post("/task/{task_id}")
async def ping_app(task_id):
    return task_id