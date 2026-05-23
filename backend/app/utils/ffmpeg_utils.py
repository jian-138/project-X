"""ffmpeg utility wrapper.

MVP: placeholder functions. Production: subprocess-based ffmpeg integration.
"""

import subprocess
from typing import List


def get_video_info(filepath: str) -> dict:
    """Get video metadata using ffprobe."""
    # TODO: Integrate ffprobe for real metadata extraction
    return {
        "duration": 15.0,
        "width": 1920,
        "height": 1080,
        "fps": 30.0,
    }


def extract_keyframes(filepath: str, output_dir: str, interval: float = 5.0) -> List[str]:
    """Extract keyframes from video at regular intervals using ffmpeg.

    Args:
        filepath: Path to the video file.
        output_dir: Directory to save extracted frames.
        interval: Time interval between frames in seconds.

    Returns:
        List of output file paths.
    """
    # TODO: Integrate ffmpeg for real frame extraction
    # ffmpeg -i {filepath} -vf "fps=1/{interval}" {output_dir}/frame_%03d.png
    return []
