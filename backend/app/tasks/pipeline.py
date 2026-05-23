"""Mock pipeline orchestration for the stable ChronoShift demo."""

import time

from .celery_app import mock_celery_task
from ..models.task import tasks_store
from ..services import (
    generate_scene_images,
    generate_voiceover,
    pack_script,
    parse_video,
    rewrite_for_era,
    understand_content,
)


def _update_task(task_id: str, phase: str, progress: int, message: str):
    if task_id in tasks_store:
        task = tasks_store[task_id]
        task.phase = phase
        task.progress = progress
        task.message = message


def _pause(seconds: float = 0.8):
    time.sleep(seconds)


@mock_celery_task
def run_pipeline(task_id: str, filepath: str, era: str):
    """Execute the full mock ChronoShift pipeline."""
    try:
        _update_task(task_id, "parsing", 5, "正在解析视频，抽取关键帧...")
        _pause()
        parse_result = parse_video(filepath, task_id)
        _update_task(task_id, "parsing", 15, "视频解析完成")
        _pause(0.5)

        _update_task(task_id, "understanding", 20, "正在分析场景、人物与叙事结构...")
        _pause()
        understanding = understand_content(parse_result["keyframes"], parse_result["transcript"])
        _update_task(task_id, "understanding", 30, "内容理解完成")
        _pause(0.5)

        _update_task(task_id, "rewriting", 35, "正在生成时代化世界观与台词...")
        _pause()
        rewrite_result = rewrite_for_era(understanding, era, parse_result["transcript"])
        _update_task(task_id, "rewriting", 45, "时代改写完成")
        _pause(0.5)

        _update_task(task_id, "generating", 55, "正在生成时代化场景图占位结果...")
        _pause()
        image_results = generate_scene_images(rewrite_result["scenes"], task_id, parse_result["keyframes"])
        _update_task(task_id, "generating", 70, "正在生成配音占位结果...")
        _pause()
        voice_results = generate_voiceover(rewrite_result["scenes"], task_id, era)
        _update_task(task_id, "generating", 80, "图片与配音结果生成完成")
        _pause(0.5)

        _update_task(task_id, "packaging", 90, "正在打包视频脚本 JSON...")
        _pause()
        script = pack_script(
            task_id,
            era,
            rewrite_result["scenes"],
            image_results,
            voice_results,
            parse_result["keyframes"],
        )
        _update_task(task_id, "done", 100, f"完成，共生成 {len(script.scenes)} 个场景")

    except Exception as exc:
        _update_task(task_id, "failed", 0, "任务处理失败")
        if task_id in tasks_store:
            tasks_store[task_id].error = str(exc)
