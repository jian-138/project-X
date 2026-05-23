import os
import uuid

import aiofiles
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..config import settings
from ..models.task import TaskStatus, tasks_store
from ..tasks.pipeline import run_pipeline

router = APIRouter()


@router.post("/upload")
async def upload_video(file: UploadFile = File(...), era: str = Form(...)):
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(400, "仅支持视频文件")

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, f"文件大小超过 {settings.MAX_UPLOAD_SIZE_MB}MB 限制")

    task_id = str(uuid.uuid4())[:8]
    ext = os.path.splitext(file.filename or "video.mp4")[1] or ".mp4"
    filename = f"{task_id}{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)

    async with aiofiles.open(filepath, "wb") as saved_file:
        await saved_file.write(content)

    tasks_store[task_id] = TaskStatus(
        task_id=task_id,
        phase="queued",
        progress=0,
        message="任务已提交，等待处理",
    )

    run_pipeline.delay(task_id, filepath, era)

    return {
        "task_id": task_id,
        "filename": file.filename,
        "duration": 0,
    }
