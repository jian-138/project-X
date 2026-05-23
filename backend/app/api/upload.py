import os
import uuid

import aiofiles
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..config import settings
from ..models.task import TaskStatus, tasks_store
from ..services import (
    create_initial_conversation,
    generate_script_images,
    parse_video,
    save_conversation,
    understand_content,
)

router = APIRouter()


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    era: str = Form(...),
    creative_brief: str = Form(""),
    api_key: str = Form(""),
):
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
        phase="rewriting",
        progress=35,
        message="OpenAI 多角色创作室正在生成初版脚本",
    )

    try:
        parse_result = parse_video(filepath, task_id)
        understanding = understand_content(parse_result["keyframes"], parse_result["transcript"])
        conversation = create_initial_conversation(
            task_id=task_id,
            era=era,
            creative_brief=creative_brief,
            transcript=parse_result["transcript"],
            understanding=understanding,
            api_key=api_key,
        )
        if conversation.script:
            tasks_store[task_id].phase = "generating"
            tasks_store[task_id].progress = 70
            tasks_store[task_id].message = "正在使用 GPT 快速模型生成场景图"
            conversation.script = generate_script_images(conversation.script, api_key)

        save_conversation(conversation)
    except Exception as exc:
        tasks_store[task_id] = TaskStatus(
            task_id=task_id,
            phase="failed",
            progress=0,
            message="OpenAI 生成失败",
            error=str(exc),
        )
        raise HTTPException(500, str(exc)) from exc

    tasks_store[task_id] = TaskStatus(
        task_id=task_id,
        phase="done",
        progress=100,
        message="多角色剧情脚本与场景图已生成",
    )

    return {
        "task_id": task_id,
        "filename": file.filename,
        "duration": parse_result["duration"],
    }
