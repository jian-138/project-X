"""Script packer service — combine all outputs into a structured video script."""

import os
import json
from datetime import datetime, timezone
from ..config import settings
from ..models.script import VideoScript, Scene


def pack_script(
    task_id: str,
    era: str,
    scenes_data: list,
    image_results: list,
    voice_results: list,
    keyframes: list,
) -> VideoScript:
    """Pack all generated assets into a VideoScript and save as JSON."""
    scenes = []
    for scene in scenes_data:
        idx = scene["index"]
        img = next((r for r in image_results if r["index"] == idx), {})
        voice = next((r for r in voice_results if r["index"] == idx), {})
        kf = keyframes[idx] if idx < len(keyframes) else {"timestamp": idx * 5.0, "path": ""}

        scenes.append(Scene(
            index=idx,
            timestamp=kf["timestamp"],
            original_frame=kf["path"],
            generated_frame=img.get("generated_frame", ""),
            dialogue=scene["dialogue"],
            voice_url=voice.get("voice_url", ""),
            transition=scene.get("transition", "cut"),
        ))

    script = VideoScript(
        task_id=task_id,
        era=era,
        scenes=scenes,
        bgm_url=None,  # Reserved for future BGM integration
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    # Save to disk
    out_dir = os.path.join(settings.OUTPUT_DIR, task_id)
    os.makedirs(out_dir, exist_ok=True)
    script_path = os.path.join(out_dir, "script.json")
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script.model_dump(), f, ensure_ascii=False, indent=2)

    return script
