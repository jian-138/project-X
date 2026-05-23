from fastapi import APIRouter, HTTPException

from ..services import load_script

router = APIRouter()


@router.get("/result/{task_id}")
def get_result(task_id: str):
    try:
        script = load_script(task_id)
    except FileNotFoundError as exc:
        raise HTTPException(404, "结果文件不存在") from exc

    return {"task_id": task_id, "script": script}


@router.post("/task/{task_id}/bgm")
def match_bgm(task_id: str):
    return {
        "task_id": task_id,
        "bgm_url": "",
        "status": "placeholder",
        "message": "BGM 匹配功能已预留，当前版本返回占位数据。",
    }


@router.post("/task/{task_id}/synthesize")
def synthesize_video(task_id: str):
    return {
        "task_id": task_id,
        "video_url": "",
        "status": "placeholder",
        "message": "视频合成功能已预留，当前版本返回占位数据。",
    }
