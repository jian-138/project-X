from .celery_app import MockTask, mock_celery_task
from .pipeline import run_pipeline

celery_app = None  # MVP: synchronous execution, no Celery broker needed

__all__ = ["celery_app", "run_pipeline", "MockTask", "mock_celery_task"]
