from fastapi import APIRouter, HTTPException

from ..models.conversation import ConversationStepRequest
from ..models.task import TaskStatus, tasks_store
from ..services import (
    continue_conversation,
    generate_script_images,
    load_conversation,
    parse_video,
    save_conversation,
    understand_content,
)

router = APIRouter()


@router.get("/conversation/{task_id}")
def get_conversation(task_id: str):
    try:
        conversation = load_conversation(task_id)
    except FileNotFoundError as exc:
        raise HTTPException(404, "会话不存在") from exc

    return {"task_id": task_id, "conversation": conversation}


@router.post("/conversation/{task_id}/step")
def step_conversation(task_id: str, request: ConversationStepRequest):
    try:
        state = load_conversation(task_id)
    except FileNotFoundError as exc:
        raise HTTPException(404, "会话不存在") from exc

    if not request.feedback.strip():
        raise HTTPException(400, "反馈内容不能为空")

    tasks_store[task_id] = TaskStatus(
        task_id=task_id,
        phase="rewriting",
        progress=60,
        message="正在根据用户反馈继续创作",
    )

    try:
        parse_result = parse_video("uploaded-video-placeholder.mp4", task_id)
        understanding = understand_content(parse_result["keyframes"], parse_result["transcript"])
        next_state = continue_conversation(
            state=state,
            feedback=request.feedback,
            transcript=parse_result["transcript"],
            understanding=understanding,
            api_key=request.api_key,
        )
        if next_state.script:
            tasks_store[task_id].phase = "generating"
            tasks_store[task_id].progress = 80
            tasks_store[task_id].message = "正在为改稿后的脚本生成场景图"
            next_state.script = generate_script_images(next_state.script, request.api_key)

        save_conversation(next_state)
    except Exception as exc:
        tasks_store[task_id] = TaskStatus(
            task_id=task_id,
            phase="failed",
            progress=0,
            message="OpenAI 改稿失败",
            error=str(exc),
        )
        raise HTTPException(500, str(exc)) from exc

    tasks_store[task_id] = TaskStatus(
        task_id=task_id,
        phase="done",
        progress=100,
        message="剧情脚本与场景图已更新",
    )

    return {"task_id": task_id, "conversation": next_state}
