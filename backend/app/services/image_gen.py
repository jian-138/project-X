"""Image generation service.

MVP: returns mock output paths. Production: Flux / Wan / Kling API.
"""


def generate_scene_images(scenes: list, task_id: str, keyframes: list) -> list:
    """Generate mock image metadata for each rewritten scene."""
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
