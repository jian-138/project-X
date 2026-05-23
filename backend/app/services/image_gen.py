"""Image generation service powered by OpenAI GPT image models."""

import base64
import os

from ..config import settings
from ..models.script import VideoScript


def _api_key(explicit_api_key: str | None) -> str:
    key = (explicit_api_key or "").strip() or settings.OPENAI_API_KEY
    if not key:
        raise ValueError("缺少 OpenAI API Key，无法生成图片。")
    return key


def _scene_prompt(script: VideoScript, scene_index: int, dialogue: str) -> str:
    beats = "；".join(script.story_beats or [])
    return (
        "Create a cinematic vertical short-video keyframe concept art. "
        f"Era/style: {script.era}. "
        f"Story title: {script.title or 'ChronoShift scene'}. "
        f"Story summary: {script.summary or ''}. "
        f"Story beats: {beats}. "
        f"Scene {scene_index + 1} dialogue: {dialogue}. "
        "Show the scene as a polished era-transformed image, no text, no subtitles, "
        "strong composition, expressive characters, visually coherent with the era."
    )


def generate_script_images(script: VideoScript, api_key: str | None = None) -> VideoScript:
    """Generate one PNG image for each script scene and update generated_frame paths."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("后端缺少 openai Python SDK，请先安装 requirements.txt。") from exc

    client = OpenAI(api_key=_api_key(api_key))
    output_dir = os.path.join(settings.OUTPUT_DIR, script.task_id)
    os.makedirs(output_dir, exist_ok=True)

    for scene in script.scenes:
        response = client.images.generate(
            model=settings.OPENAI_IMAGE_MODEL,
            prompt=_scene_prompt(script, scene.index, scene.dialogue),
            size="1024x1024",
            quality="low",
            n=1,
        )
        item = response.data[0]
        image_b64 = getattr(item, "b64_json", None)
        if not image_b64:
            raise RuntimeError("OpenAI 图片接口没有返回 base64 图片数据。")

        filename = f"scene_{scene.index:03d}.png"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as image_file:
            image_file.write(base64.b64decode(image_b64))

        scene.generated_frame = f"outputs/{script.task_id}/{filename}"

    return script


def generate_scene_images(scenes: list, task_id: str, keyframes: list) -> list:
    """Compatibility helper for the old mock pipeline."""
    results = []
    for scene in scenes:
        index = scene["index"]
        results.append({
            "index": index,
            "original_frame": keyframes[index]["path"] if index < len(keyframes) else "",
            "generated_frame": f"outputs/{task_id}/scene_{index:03d}.png",
        })
    return results


def generate_bgm(era: str, task_id: str) -> str:
    """Reserved interface for future BGM generation or matching."""
    return ""
