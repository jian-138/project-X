from .upload import router as upload_router
from .task import router as task_router
from .result import router as result_router

__all__ = ["upload_router", "task_router", "result_router"]
