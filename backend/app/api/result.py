import json
import os

from fastapi import APIRouter, HTTPException

from ..config import settings
from ..models.task import tasks_store

router = APIRouter()


@router.get("/result/{task_id}")
def get_result(task_id: str):
    if task_id not in tasks_store:
        raise HTTPException(404, "任务不存在")

    task = tasks_store[task_id]
    if task.phase == "failed":
        raise HTTPException(500, f"任务失败：{task.error}")
    if task.phase != "done":
        raise HTTPException(400, "任务尚未完成")

    script_path = os.path.join(settings.OUTPUT_DIR, task_id, "script.json")
    if not os.path.exists(script_path):
        raise HTTPException(404, "结果文件不存在")

    with open(script_path, "r", encoding="utf-8") as script_file:
        data = json.load(script_file)

    return {"task_id": task_id, "script": data}


@router.post("/task/{task_id}/bgm")
def match_bgm(task_id: str):
    if task_id not in tasks_store:
        raise HTTPException(404, "任务不存在")
    return {
        "task_id": task_id,
        "bgm_url": "",
        "status": "placeholder",
        "message": "BGM 匹配功能已预留，当前演示版本返回占位数据。",
    }


@router.post("/task/{task_id}/synthesize")
def synthesize_video(task_id: str):
    if task_id not in tasks_store:
        raise HTTPException(404, "任务不存在")
    return {
        "task_id": task_id,
        "video_url": "",
        "status": "placeholder",
        "message": "视频合成功能已预留，当前演示版本返回占位数据。",
    }
