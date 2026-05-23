# ChronoShift — 平行时代转换器

让每一段短视频，都能穿越到另一个时代。

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | Next.js 15 + React 19 + TypeScript + Tailwind CSS 4 + Framer Motion |
| 后端 | FastAPI + Python 3.14 + Celery + Redis |
| 视频处理 | ffmpeg + OpenCV |
| 语音识别 | Whisper |
| 多模态理解 | Gemini / GPT-4o |
| 图像生成 | Flux / Wan / Kling |
| TTS | CosyVoice / FishSpeech |

## 项目结构

```
├── frontend/          # Next.js 前端
│   └── src/
│       ├── app/       # 页面路由（首页 / 处理中 / 结果）
│       ├── components/# 共享组件
│       └── lib/       # API 封装 + 类型定义
├── backend/           # FastAPI 后端
│   └── app/
│       ├── api/       # REST API 路由
│       ├── models/    # Pydantic 数据模型
│       ├── services/  # 业务服务（理解/改写/生图/TTS/打包）
│       ├── tasks/     # Celery 任务编排
│       └── utils/     # ffmpeg + 文件工具
└── docs/              # 产品文档
```

## 快速开始

### 环境要求

- Node.js >= 18
- Python >= 3.12
- ffmpeg (视频处理)
- Redis (任务队列，可选 — MVP 阶段使用内存存储)

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入 API Key
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档。

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000 使用应用。

### 3. API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/upload` | 上传视频，提交转换任务 |
| GET | `/api/task/{task_id}` | 查询任务状态与进度 |
| GET | `/api/result/{task_id}` | 获取生成的视频脚本 |
| POST | `/api/task/{task_id}/bgm` | 背景音乐匹配（预留） |
| POST | `/api/task/{task_id}/synthesize` | 视频合成（预留） |

## MVP 范围

- 视频上传与关键帧抽取
- 多模态内容理解
- 时代改写（6 个时代模板：古希腊/拿破仑/唐朝/中世纪酒馆/赛博朋克/维多利亚）
- 场景图片生成 + TTS 配音
- 视频脚本打包输出（JSON）
- 对比展示页面
- 背景音乐与视频合成接口预留

## License

MIT
