from fastapi import APIRouter, HTTPException

from ..models.task import tasks_store

router = APIRouter()


@router.get("/task/{task_id}")
def get_task_status(task_id: str):
    if task_id not in tasks_store:
        raise HTTPException(404, "任务不存在")
    return tasks_store[task_id]
