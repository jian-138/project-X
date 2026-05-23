from typing import Literal

from pydantic import BaseModel, Field

from .script import VideoScript

ConversationStatus = Literal["drafting", "ready", "failed"]


class ConversationMessage(BaseModel):
    role: str
    phase: str
    content: str
    created_at: str


class ConversationState(BaseModel):
    task_id: str
    era: str
    creative_brief: str = ""
    status: ConversationStatus = "drafting"
    messages: list[ConversationMessage] = Field(default_factory=list)
    script: VideoScript | None = None
    updated_at: str = ""
    error: str | None = None


class ConversationResponse(BaseModel):
    task_id: str
    conversation: ConversationState


class ConversationStepRequest(BaseModel):
    feedback: str
    api_key: str | None = None


class ConversationStepResponse(BaseModel):
    task_id: str
    conversation: ConversationState
