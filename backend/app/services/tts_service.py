"""TTS service.

MVP: returns mock audio paths. Production: CosyVoice / FishSpeech integration.
"""


def generate_voiceover(scenes: list, task_id: str, era: str) -> list:
    """Generate mock voiceover metadata for each scene."""
    return [
        {
            "index": scene["index"],
            "voice_url": f"outputs/{task_id}/voice_{scene['index']:03d}.wav",
            "voice_style": era,
        }
        for scene in scenes
    ]
