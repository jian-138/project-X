"""File utility functions."""

import os
import shutil


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def cleanup_temp(task_id: str, upload_dir: str, output_dir: str):
    """Clean up temporary files after task completion or timeout."""
    # Keep output, remove upload temp
    upload_path = os.path.join(upload_dir, task_id)
    if os.path.exists(upload_path):
        shutil.rmtree(upload_path, ignore_errors=True)
