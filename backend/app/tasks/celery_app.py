"""Minimal background task wrapper for the local MVP demo.

The production plan still targets Celery + Redis. For the stable demo loop we
run tasks in a daemon thread so uploads return immediately without external
infrastructure.
"""

import os
import threading

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/0")


class MockAsyncResult:
    def __init__(self, thread: threading.Thread):
        self.thread = thread


class MockTask:
    def __init__(self, func):
        self.func = func

    def delay(self, *args, **kwargs):
        thread = threading.Thread(target=self.func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return MockAsyncResult(thread)


def mock_celery_task(func):
    return MockTask(func)
