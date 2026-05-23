from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class Scene(BaseModel):
    index: int
    timestamp: float
    original_frame: str
    generated_frame: str
    dialogue: str
    voice_url: str
    transition: str


class VideoScript(BaseModel):
    task_id: str
    era: str
    scenes: List[Scene]
    bgm_url: str | None = None
    created_at: str = ""
