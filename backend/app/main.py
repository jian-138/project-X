from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api import conversation, result, task, upload
from .config import settings

app = FastAPI(
    title="ChronoShift API",
    description="平行时代转换器后端服务",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(task.router, prefix="/api", tags=["task"])
app.include_router(result.router, prefix="/api", tags=["result"])
app.include_router(conversation.router, prefix="/api", tags=["conversation"])


@app.get("/")
def root():
    return {"service": "ChronoShift API", "version": "0.1.0"}
