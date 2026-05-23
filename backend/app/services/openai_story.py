import json
from datetime import datetime, timezone
from typing import Any

from ..config import settings
from ..models.conversation import ConversationMessage, ConversationState
from ..models.script import Scene, VideoScript

ROLE_NAMES = ["导演", "编剧", "美术指导", "配音导演", "整合者"]

STORY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["messages", "script"],
    "properties": {
        "messages": {
            "type": "array",
            "minItems": 3,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["role", "phase", "content"],
                "properties": {
                    "role": {"type": "string"},
                    "phase": {"type": "string"},
                    "content": {"type": "string"},
                },
            },
        },
        "script": {
            "type": "object",
            "additionalProperties": False,
            "required": ["title", "summary", "story_beats", "scenes"],
            "properties": {
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "story_beats": {"type": "array", "items": {"type": "string"}},
                "scenes": {
                    "type": "array",
                    "minItems": 3,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["index", "timestamp", "dialogue", "transition"],
                        "properties": {
                            "index": {"type": "integer"},
                            "timestamp": {"type": "number"},
                            "dialogue": {"type": "string"},
                            "transition": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _api_key(explicit_api_key: str | None) -> str:
    key = (explicit_api_key or "").strip() or settings.OPENAI_API_KEY
    if not key:
        raise ValueError("缺少 OpenAI API Key。请在页面输入 API Key，或在后端 .env 配置 OPENAI_API_KEY。")
    return key


def _json_from_response(response: Any) -> dict:
    text = getattr(response, "output_text", None)
    if text:
        return json.loads(text)

    for output in getattr(response, "output", []) or []:
        for content in getattr(output, "content", []) or []:
            value = getattr(content, "text", None)
            if value:
                return json.loads(value)

    raise ValueError("OpenAI 返回为空，无法生成剧情脚本。")


def _call_openai(prompt: str, api_key: str) -> dict:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("后端缺少 openai Python SDK，请先安装 requirements.txt。") from exc

    client = OpenAI(api_key=api_key)
    last_error: Exception | None = None

    for _ in range(2):
        try:
            response = client.responses.create(
                model=settings.OPENAI_MODEL,
                input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "chronoshift_story_room",
                        "schema": STORY_SCHEMA,
                        "strict": True,
                    }
                },
            )
            return _json_from_response(response)
        except Exception as exc:
            last_error = exc

    message = str(last_error) if last_error else "未知 OpenAI 错误"
    raise RuntimeError(f"OpenAI 生成失败：{message}")


def _prompt(
    *,
    era: str,
    creative_brief: str,
    transcript: str,
    understanding: dict,
    previous_state: ConversationState | None = None,
    feedback: str | None = None,
) -> str:
    previous_summary = ""
    if previous_state:
        recent_messages = previous_state.messages[-8:]
        previous_summary = "\n".join(
            f"{message.role}({message.phase}): {message.content}" for message in recent_messages
        )
        if previous_state.script:
            previous_summary += "\n当前脚本摘要：" + (previous_state.script.summary or "")

    return f"""
你是 ChronoShift 的分布式剧情创作团队。请用中文输出。

目标时代：{era}
用户创作要求：{creative_brief or "无特别要求，保持短视频原意并增强戏剧性。"}
原视频转写：{transcript}
视频理解：{json.dumps(understanding, ensure_ascii=False)}

角色必须包含：{", ".join(ROLE_NAMES)}。
要求：
1. 让多角色像创作会议一样轮流提出建议，不要只输出最终脚本。
2. 导演负责故事方向，编剧负责冲突和结构，美术指导负责时代化画面，配音导演负责语言风格，整合者负责落成脚本。
3. 输出 3 个短视频场景，每个场景台词适合被朗读，能直接显示在结果页。
4. 保留原视频“探店/体验/推荐”的核心，但让它在目标时代中合理存在。
5. 严格按 JSON schema 输出，不要输出 Markdown。

已有创作记录：
{previous_summary or "暂无，正在生成第一轮。"}

用户最新反馈：
{feedback or "暂无，生成初版。"}
""".strip()


def _state_from_payload(task_id: str, era: str, creative_brief: str, payload: dict) -> ConversationState:
    messages = [
        ConversationMessage(
            role=item["role"],
            phase=item["phase"],
            content=item["content"],
            created_at=_now(),
        )
        for item in payload["messages"]
    ]

    scenes = [
        Scene(
            index=item["index"],
            timestamp=item["timestamp"],
            original_frame=f"uploads/{task_id}/frame_{item['index']:03d}.png",
            generated_frame=f"outputs/{task_id}/scene_{item['index']:03d}.png",
            dialogue=item["dialogue"],
            voice_url=f"outputs/{task_id}/voice_{item['index']:03d}.wav",
            transition=item["transition"],
        )
        for item in payload["script"]["scenes"]
    ]

    script = VideoScript(
        task_id=task_id,
        era=era,
        scenes=scenes,
        bgm_url=None,
        created_at=_now(),
        title=payload["script"]["title"],
        summary=payload["script"]["summary"],
        story_beats=payload["script"]["story_beats"],
    )

    return ConversationState(
        task_id=task_id,
        era=era,
        creative_brief=creative_brief,
        status="ready",
        messages=messages,
        script=script,
        updated_at=_now(),
    )


def create_initial_conversation(
    *,
    task_id: str,
    era: str,
    creative_brief: str,
    transcript: str,
    understanding: dict,
    api_key: str | None,
) -> ConversationState:
    payload = _call_openai(
        _prompt(
            era=era,
            creative_brief=creative_brief,
            transcript=transcript,
            understanding=understanding,
        ),
        _api_key(api_key),
    )
    return _state_from_payload(task_id, era, creative_brief, payload)


def continue_conversation(
    *,
    state: ConversationState,
    feedback: str,
    transcript: str,
    understanding: dict,
    api_key: str | None,
) -> ConversationState:
    payload = _call_openai(
        _prompt(
            era=state.era,
            creative_brief=state.creative_brief,
            transcript=transcript,
            understanding=understanding,
            previous_state=state,
            feedback=feedback,
        ),
        _api_key(api_key),
    )
    next_state = _state_from_payload(state.task_id, state.era, state.creative_brief, payload)
    next_state.messages = state.messages + [
        ConversationMessage(role="用户", phase="反馈", content=feedback, created_at=_now())
    ] + next_state.messages
    return next_state
