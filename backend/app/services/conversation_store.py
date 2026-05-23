import json
import os
from datetime import datetime, timezone

from ..config import settings
from ..models.conversation import ConversationState
from ..models.script import VideoScript


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def task_output_dir(task_id: str) -> str:
    path = os.path.join(settings.OUTPUT_DIR, task_id)
    os.makedirs(path, exist_ok=True)
    return path


def conversation_path(task_id: str) -> str:
    return os.path.join(task_output_dir(task_id), "conversation.json")


def script_path(task_id: str) -> str:
    return os.path.join(task_output_dir(task_id), "script.json")


def save_conversation(state: ConversationState) -> None:
    state.updated_at = utc_now()
    with open(conversation_path(state.task_id), "w", encoding="utf-8") as output_file:
        json.dump(state.model_dump(), output_file, ensure_ascii=False, indent=2)

    if state.script:
        save_script(state.script)


def load_conversation(task_id: str) -> ConversationState:
    path = conversation_path(task_id)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Conversation not found: {task_id}")
    with open(path, "r", encoding="utf-8") as input_file:
        return ConversationState.model_validate(json.load(input_file))


def save_script(script: VideoScript) -> None:
    with open(script_path(script.task_id), "w", encoding="utf-8") as output_file:
        json.dump(script.model_dump(), output_file, ensure_ascii=False, indent=2)


def load_script(task_id: str) -> VideoScript:
    path = script_path(task_id)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Script not found: {task_id}")
    with open(path, "r", encoding="utf-8") as input_file:
        return VideoScript.model_validate(json.load(input_file))
