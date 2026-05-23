"""Video parsing service.

MVP: returns mock keyframes and transcript. Production: ffmpeg + Whisper.
"""

import os


def parse_video(filepath: str, task_id: str) -> dict:
    """Return a deterministic mock parsing result for demo use."""
    filename = os.path.basename(filepath)
    return {
        "source_filename": filename,
        "keyframes": [
            {"timestamp": 0.0, "path": f"uploads/{task_id}/frame_000.png"},
            {"timestamp": 5.0, "path": f"uploads/{task_id}/frame_005.png"},
            {"timestamp": 10.0, "path": f"uploads/{task_id}/frame_010.png"},
        ],
        "transcript": "今天带大家来探店，这家店的环境很不错，饮品也很好喝。",
        "duration": 15.0,
        "frame_count": 3,
    }
