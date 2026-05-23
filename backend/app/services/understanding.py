"""Multimodal understanding service.

MVP: returns mock structured understanding. Production: vision LLM integration.
"""


def understand_content(keyframes: list, transcript: str) -> dict:
    """Analyze mock keyframes and transcript into a stable scene summary."""
    return {
        "scene_type": "indoor_cafe",
        "characters": [
            {"name": "主角", "role": "探店博主", "emotion": "轻松愉快"},
        ],
        "actions": ["走进店内", "介绍环境", "品尝饮品", "对镜头推荐"],
        "narrative_summary": "一位探店博主在咖啡店里体验环境、品尝饮品，并向观众推荐这家店。",
        "key_objects": ["咖啡杯", "菜单", "店内装饰", "吧台"],
        "transcript": transcript,
        "keyframe_count": len(keyframes),
    }
