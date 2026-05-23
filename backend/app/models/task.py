from typing import Dict, Literal

from pydantic import BaseModel

TaskPhase = Literal[
    "queued",
    "parsing",
    "understanding",
    "rewriting",
    "generating",
    "packaging",
    "done",
    "failed",
]


class TaskStatus(BaseModel):
    task_id: str
    phase: TaskPhase = "queued"
    progress: int = 0
    message: str = ""
    error: str | None = None


# MVP 使用内存状态；接入真实队列后替换为 Redis。
tasks_store: Dict[str, TaskStatus] = {}
