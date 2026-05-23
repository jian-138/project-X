from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import result, task, upload

app = FastAPI(
    title="ChronoShift API",
    description="平行时代转换器后端服务",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(task.router, prefix="/api", tags=["task"])
app.include_router(result.router, prefix="/api", tags=["result"])


@app.get("/")
def root():
    return {"service": "ChronoShift API", "version": "0.1.0"}
