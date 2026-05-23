"""Script packer service: combine generated metadata into video script JSON."""

import json
import os
from datetime import datetime, timezone

from ..config import settings
from ..models.script import Scene, VideoScript


def pack_script(
    task_id: str,
    era: str,
    scenes_data: list,
    image_results: list,
    voice_results: list,
    keyframes: list,
) -> VideoScript:
    """Pack all generated assets into a VideoScript and save it to disk."""
    scenes = []
    for scene in scenes_data:
        index = scene["index"]
        image = next((item for item in image_results if item["index"] == index), {})
        voice = next((item for item in voice_results if item["index"] == index), {})
        keyframe = keyframes[index] if index < len(keyframes) else {"timestamp": index * 5.0, "path": ""}

        scenes.append(Scene(
            index=index,
            timestamp=keyframe["timestamp"],
            original_frame=keyframe["path"],
            generated_frame=image.get("generated_frame", ""),
            dialogue=scene["dialogue"],
            voice_url=voice.get("voice_url", ""),
            transition=scene.get("transition", "cut"),
        ))

    script = VideoScript(
        task_id=task_id,
        era=era,
        scenes=scenes,
        bgm_url=None,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    out_dir = os.path.join(settings.OUTPUT_DIR, task_id)
    os.makedirs(out_dir, exist_ok=True)
    script_path = os.path.join(out_dir, "script.json")
    with open(script_path, "w", encoding="utf-8") as output_file:
        json.dump(script.model_dump(), output_file, ensure_ascii=False, indent=2)

    return script
