export interface Scene {
  index: number;
  timestamp: number;
  original_frame: string;
  generated_frame: string;
  dialogue: string;
  voice_url: string;
  transition: string;
}

export interface VideoScript {
  task_id: string;
  era: string;
  scenes: Scene[];
  bgm_url: string | null;
  created_at: string;
  title?: string | null;
  summary?: string | null;
  story_beats?: string[];
}

export interface ConversationMessage {
  role: string;
  phase: string;
  content: string;
  created_at: string;
}

export interface ConversationState {
  task_id: string;
  era: string;
  creative_brief: string;
  status: "drafting" | "ready" | "failed";
  messages: ConversationMessage[];
  script: VideoScript | null;
  updated_at: string;
  error: string | null;
}

export type TaskPhase =
  | "queued"
  | "parsing"
  | "understanding"
  | "rewriting"
  | "generating"
  | "packaging"
  | "done"
  | "failed";

export interface TaskStatus {
  task_id: string;
  phase: TaskPhase;
  progress: number;
  message: string;
  error: string | null;
}

export interface EraOption {
  id: string;
  name: string;
  icon: string;
  description: string;
}

export const ERA_OPTIONS: EraOption[] = [
  {
    id: "ancient-greece",
    name: "古希腊",
    icon: "🏛️",
    description: "哲学辩论与史诗叙事",
  },
  {
    id: "napoleonic",
    name: "拿破仑时代",
    icon: "🎖️",
    description: "19 世纪欧洲纪实风格",
  },
  {
    id: "tang-dynasty",
    name: "唐朝",
    icon: "🏮",
    description: "盛唐风华与诗意表达",
  },
  {
    id: "medieval-tavern",
    name: "中世纪酒馆",
    icon: "🍻",
    description: "冒险故事与酒馆氛围",
  },
  {
    id: "cyberpunk",
    name: "赛博朋克",
    icon: "🤖",
    description: "霓虹都市与科技叙事",
  },
  {
    id: "victorian",
    name: "维多利亚时代",
    icon: "🎩",
    description: "蒸汽工业与古典优雅",
  },
];

export interface UploadResponse {
  task_id: string;
  filename: string;
  duration: number;
}

export interface ResultResponse {
  task_id: string;
  script: VideoScript;
}

export interface ConversationResponse {
  task_id: string;
  conversation: ConversationState;
}

export interface BgmResponse {
  task_id: string;
  bgm_url: string;
  status: "placeholder";
  message: string;
}

export interface SynthesizeResponse {
  task_id: string;
  video_url: string;
  status: "placeholder";
  message: string;
}
